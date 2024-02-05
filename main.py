from collections import UserDict
from datetime import datetime, date
import json

class Field:
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return str(self.__value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

class Name(Field):
    def __init__(self, name):
        super().__init__(name)

class Phone(Field):
    def validate(self, phone):
        return len(phone) == 10 and phone.isdigit()

    def __init__(self, value):
        if self.validate(value):
            super().__init__(value)
        else:
            raise ValueError("Invalid phone number")

class Birthday(Field):
    def __init__(self, birthday=None):
        super().__init__(birthday)
        if birthday:
            try:
                self.__value = datetime.strptime(birthday, "%d-%m-%Y").date()
            except ValueError:
                raise ValueError("Incorrect birthday format")

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        return f"Phone: {phone} not found"

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError(f"Phone {old_phone} not found in record.")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def days_to_birthday(self):
        if self.birthday.value is not None:
            today = date.today()
            user_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day).date()
            next_birthday = user_birthday.replace(year=today.year)

            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)

            number_of_days = (next_birthday - today).days
            return number_of_days if number_of_days != 0 else 365
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Record with name: {name} deleted"
        return f"Name: {name} not found"

    def iterator(self, item_number):
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += f'{item}: {record}\n'
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ''

    def dump(self):
        with open(self.file, 'wb') as file:
            json.dump((self.record_id, self.record), file)

    def load(self):
        if not self.file.exists():
            return
        with open(self.file, 'rb') as file:
            self.record_id, self.record = json.load(file)

    def do_search(self, line):
        search_string = input("Введіть рядок пошуку: ")
        search_results = self.address_book.search(search_string.strip())
        if search_results:
            print("Результати пошуку:")
            for result in search_results:
                print(result)
        else:
            print("Контакти не знайдено.")