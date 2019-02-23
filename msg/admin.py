from django.contrib import admin
from .models import MsgType, Msg
@admin.register(MsgType)
class MsgTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(Msg)
class MsgAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_read_num', 'created_time', 'unit', 'msg_type', 'commander',
                    'commander_phone', 'chief_duty', 'chief_phone',
                    'operator', 'operator_phone', 'registered_police',
                    'police_duty', 'emergency_police', 'emergency_vehicle',
                    'external_transfer', 'num_workers', 'training_all',
                    'training_day', 'confinement_all', 'confinement_day',
                    'isolation_all', 'isolation_day', 'death',
                    'leave_and_back', 'judicial_all', 'judicial_day',
                    'social_all', 'social_day', 'freed_people', 'parole',
                    'reconfirm', 'outside_prison', 'outside_prison_death',
                    'charter', 'detective_relatives_all',
                    'detective_relatives_day', 'foreign_workers',
                    'exotic_vehicle', 'video_alarm', 'perimeter_alarm',
                    'grid_alarm', 'violation_msg', 'leave_prison_msg',
                    'important_msg', 'emergencies_msg', 'disposal_msg',
                    'Operator', 'last_updated_time')
