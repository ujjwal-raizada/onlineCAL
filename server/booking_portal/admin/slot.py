import datetime

from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.translation import gettext_lazy
from rangefilter.filter import DateRangeFilter

from ..forms.adminForms import BulkTimeSlotForm
from ..models import Instrument, Slot


class SlotFilterByInstrument(admin.SimpleListFilter):
    # Name to be displayed on the admin portal
    title = gettext_lazy("Instrument")

    parameter_name = 'instrument'

    def lookups(self, request, model_admin):
        """Returns a list of tuples. The first element
        in each tuple is the coded value for the option
        that will appear in the URL query. The second value
        is the human-readable name for the option that will
        appear in the right side bar"""

        return (
            (instr.id, gettext_lazy(str(instr)))
            for instr in Instrument.objects.all()
        )

    def queryset(self, request, queryset):
        """Returns the filtered queryset based on the
        value provided in the query string and retrievable
        via `self.value()`"""

        return (
            queryset if self.value() is None
            else queryset.filter(instrument__id=self.value())
        )


class SlotAdmin(admin.ModelAdmin):
    change_list_template = "admin/slot_change_list.html"
    list_filter = (
        ('date', DateRangeFilter),
        'status',
        SlotFilterByInstrument
    )
    list_display = admin.ModelAdmin.list_display + ('status',)

    # 'Add Slot' button is only visible to the admin
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def time_left(self, current, end, duration):
        """Checks if a slot can be made with `current time` and
        `duration` before the `end time`"""
        today = datetime.date.today()
        diff = (datetime.datetime.combine(today, end) -
                datetime.datetime.combine(today, current))

        return (diff >= duration)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("bulk-slots/", self.generate_slots),
        ]
        return my_urls + urls

    def render_bulk_slots_form(self, request, form):
        payload = {"form": form}
        return render(request, "admin/bulk_import_slots_form.html", payload)

    def generate_slots(self, request):
        """Bulk Import Slots has a form for creating slots.
        This form is restricted to staff.
        """
        # TODO: Check time slot overlap

        INTERVAL_CHOICES = {
            "1-hour": datetime.timedelta(hours=1),
            "2-hour": datetime.timedelta(hours=2),
            "3-hour": datetime.timedelta(hours=3),
            "4-hour": datetime.timedelta(hours=4),
            "6-hour": datetime.timedelta(hours=6),
            "8-hour": datetime.timedelta(hours=8),
        }

        if request.method == 'POST':
            form = BulkTimeSlotForm(request.POST)
            if not form.is_valid():
                messages.error(request, "Invalid form data!")
                return self.render_bulk_slots_form(request, form)

            instr = form.cleaned_data['instruments']
            start_date = form.cleaned_data['start_date']
            start_time = int(form.cleaned_data['start_time'].split(':')[0])
            end_time = int(form.cleaned_data['end_time'].split(':')[0])
            duration = INTERVAL_CHOICES.get(form.cleaned_data['lab_duration'], None)
            # number of days for which the timeslot has to be made
            delta = int(form.cleaned_data['for_the_next'])

            # handle exceptional cases
            if start_time >= end_time:
                messages.error(request, "Start time cannot be greater than end time!")
                return self.render_bulk_slots_form(request, form)
            elif duration is None:
                messages.error(request, "Duration cannot be empty!")
                return self.render_bulk_slots_form(request, form)
            elif start_date < datetime.date.today():
                messages.error(request, "Start date cannot be before today")
                return self.render_bulk_slots_form(request, form)

            # get the next `delta` days after `today`
            next_days = [start_date + datetime.timedelta(days=var) for var in range(0, delta)]
            # remove the sundays, these two lines can be merged using the walrus op
            next_days = [day for day in next_days if not day.weekday() == 6]

            if not next_days:
                messages.error(request, "The list of days to create slots is empty! Note that slots that fall on "
                                        "Sunday are removed.")
                return self.render_bulk_slots_form(request, form)


            # generate datetime objects for the next `delta` days
            all_slots = {}
            for day in next_days:
                day_wise = []
                current = datetime.time(hour=start_time)
                end = datetime.time(hour=end_time)
                while current < end and self.time_left(current, end, duration):
                    day_wise.append(datetime.datetime.combine(day, current))
                    current = datetime.time(hour=(datetime.datetime.combine(day, current) + duration).hour)
                all_slots[day] = day_wise

            for day, time_slots in all_slots.items():
                for time_slot in time_slots:
                    # Check if the slot already exists
                    if not Slot.objects.filter(
                            duration=duration,
                            instrument=instr,
                            date=day,
                            time=time_slot.time(),
                    ).exists():
                        slot_obj = Slot(
                            duration=duration,
                            instrument=instr,
                            status=Slot.STATUS_1,
                            date=day,
                            time=time_slot.time()
                        )
                        slot_obj.save()

            messages.success(request, "Slots successfully created!")
            return redirect("..")
        else:
            form = BulkTimeSlotForm()
            return self.render_bulk_slots_form(request, form)
