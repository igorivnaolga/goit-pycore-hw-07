from collections import UserDict
import re
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    

class Name(Field):
		pass


class Phone(Field):
    def __init__(self, value):
           if not re.fullmatch(r"\d{10}", value):
                  raise ValueError("Phone number must contain 10 digits")
           super().__init__(value)


class Birthday(Field):
      def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
           self.phones.append(Phone(phone))
    
    def remove_phone(self, phone):
          for ph in self.phones:
                if ph.value == phone:
                      self.phones.remove(ph)

    def edit_phone(self, old_phone, new_phone):
        for ph in self.phones:
            if ph.value == old_phone:
                ph.value == new_phone
                return True
        return False
    
    def find_phone(self, phone):
          for ph in self.phones:
                if ph.value == phone:
                      return ph
          return None
    
    def add_birthday(self, birthday):
         self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Contact name: {self.name}, phones: {phones_str}{birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
          self.data[record.name.value] = record

    def find(self, name):
          return self.data.get(name)
    
    def delete(self, name):
          if name in self.data:
                del self.data[name]

    def get_upcoming_birthdays(self):
        current_day = datetime.today().date()
        upcoming_birthdays = []
        
        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=current_day.year)
                if birthday_this_year < current_day:
                    birthday_this_year = birthday_this_year.replace(year=current_day.year + 1)
                
                days_before_birthday = (birthday_this_year - current_day).days
                
                if 0 <= days_before_birthday <= 7:
                    if birthday_this_year.weekday() == 5:  # Saturday
                        birthday_this_year += timedelta(days=2)
                    elif birthday_this_year.weekday() == 6:  # Sunday
                        birthday_this_year += timedelta(days=1)
                
                    
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": birthday_this_year.strftime("%d.%m.%Y")
                    })
        
        return upcoming_birthdays



# Тестування системи
if __name__ == "__main__":
    book = AddressBook()
    
    # Додавання контактів
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("23.03.1990")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("25.03.1985")
    book.add_record(jane_record)
    
    # Виведення всіх контактів
    for record in book.data.values():
        print(record)
    
    # Пошук та редагування телефону
    john = book.find("John")
    if john:
        john.edit_phone("1234567890", "1112223333")
    print(john)
    
    # Пошук телефону
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")
    
    # Видалення контакту
    # book.delete("Jane")
    
    # Виведення найближчих днів народження
    print("Upcoming birthdays:", book.get_upcoming_birthdays())
