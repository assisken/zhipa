import json
import os
from collections import namedtuple

from smiap.settings import BASE_DIR

FILE_PATH = '/home/aken/Downloads/staff.json'

Staff = namedtuple('Staff', 'pk lastname firstname middlename img regalia description leader lecturer hide')


def iter_json():
    with open(FILE_PATH, 'r') as file:
        all_staff = json.loads(file.read())
    for staff in all_staff:
        yield Staff(
            pk=staff['id'],
            lastname=staff['lastname'],
            firstname=staff['firstname'],
            middlename=staff['patronymic'],
            img=staff['img'],
            regalia=staff['regalia'],
            description=staff['description'],
            leader=staff['leader'],
            lecturer=staff['lecturer'],
            hide=staff['hide']
        )


def gen_normal_staff(staff: Staff):
    return {
               'model': 'main.staff',
               'pk': staff.pk,
               'fields': {
                   'lastname': staff.lastname,
                   'firstname': staff.firstname,
                   'middlename': staff.middlename,
                   'img': staff.img,
                   'regalia': staff.regalia,
                   'description': staff.description,
                   'leader': staff.leader,
                   'lecturer': staff.lecturer,
                   'hide': staff.hide
               }
           }


if __name__ == '__main__':
    staffs = [gen_normal_staff(staff) for staff in iter_json()]
    with open(os.path.join(BASE_DIR, 'main', 'fixtures', 'staff.json'), 'w') as file:
        file.write(json.dumps(staffs, sort_keys=True, indent=4))
