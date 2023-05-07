from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.storage.jsonstore import JsonStore
from datetime import datetime

class MainApp(App):
    def build(self):
        self.store = JsonStore('finances_csv.json')
        self.main_layout = BoxLayout(orientation="vertical")

        # Загрузить баланс, если он уже был сохранен, иначе установить его равным 0
        self.balance = self.store.get('balance')['amount'] if self.store.exists('balance') else 0

        # Поля для ввода данных
        self.income_layout = BoxLayout(orientation="horizontal")
        self.income_layout.add_widget(Label(text='Доход: '))
        self.income_input = TextInput(multiline=False)
        self.income_layout.add_widget(self.income_input)
        self.main_layout.add_widget(self.income_layout)

        self.expense_name_layout = BoxLayout(orientation="horizontal")
        self.expense_name_layout.add_widget(Label(text='Статья расхода: '))
        self.expense_name_input = TextInput(multiline=False)
        self.expense_name_layout.add_widget(self.expense_name_input)
        self.main_layout.add_widget(self.expense_name_layout)

        self.expense_layout = BoxLayout(orientation="horizontal")
        self.expense_layout.add_widget(Label(text='Расход: '))
        self.expense_input = TextInput(multiline=False)
        self.expense_layout.add_widget(self.expense_input)
        self.main_layout.add_widget(self.expense_layout)

        # Кнопка для расчета баланса
        self.calc_button = Button(text=f"Баланс: {self.balance}")
        self.calc_button.bind(on_press=self.calculate_balance)

        # Таблица для отображения данных
        self.table_layout = GridLayout(cols=4)
        self.table_layout.add_widget(Label(text='Дата'))
        self.table_layout.add_widget(Label(text='Доход'))
        self.table_layout.add_widget(Label(text='Статья расхода'))
        self.table_layout.add_widget(Label(text='Расход'))

        # Загрузка сохраненных данных в таблицу
        for key in self.store.keys():
            if key != "balance":
                try:
                    data = self.store.get(key)
                    self.table_layout.add_widget(Label(text=data['date']))
                    self.table_layout.add_widget(Label(text=data['income']))
                    self.table_layout.add_widget(Label(text=data['expense_name']))
                    self.table_layout.add_widget(Label(text=data['expense']))
                except KeyError:
                    # Если в данных отсутствуют необходимые ключи, пропустить их
                    continue

        # Вывод текущего баланса
        self.balance_label = Label(text=f'Текущий баланс: {self.balance}')

        self.main_layout.add_widget(self.calc_button)
        self.main_layout.add_widget(self.table_layout)
        self.main_layout.add_widget(self.balance_label)

        return self.main_layout

    def calculate_balance(self, instance):
        income = self.income_input.text
        expense = self.expense_input.text
        expense_name = self.expense_name_input.text

        # Если поля дохода или расхода пустые или не числовые, считать их как 0
        if income == "":
            income = 0
        else:
            try:
                income = float(income)
            except ValueError:
                income = 0

        if expense == "":
            expense = 0
        else:
            try:
                expense = float(expense)
            except ValueError:
                expense = 0

        self.balance += income - expense

        # Запись данных в таблицу
        self.table_layout.add_widget(Label(text=str(datetime.now().date())))
        self.table_layout.add_widget(Label(text=str(income)))
        self.table_layout.add_widget(Label(text=expense_name))
        self.table_layout.add_widget(Label(text=str(expense)))

        # Обновление баланса и сохранение данных
        self.balance_label.text = f'Текущий баланс: {self.balance}'
        self.calc_button.text = f'Баланс: {self.balance}'
        self.store.put('balance', amount=self.balance)

        # Сохранение данных транзакции
        self.store.put(str(datetime.now()),
                       date=str(datetime.now().date()),
                       income=str(income),
                       expense_name=expense_name,
                       expense=str(expense))

        # Очистить поля ввода
        self.income_input.text = ""
        self.expense_input.text = ""
        self.expense_name_input.text = ""


if __name__ == '__main__':
    MainApp().run()