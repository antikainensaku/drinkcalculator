import customtkinter as ctk
from dataclasses import dataclass


@dataclass
class Drink:
    number: int
    percentage: float
    volume: float


class DrinkCalculator(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry('800x600')
        self.title('Drink Calculator')
        self.drinks = {}
        self.total_volume = 0
        self.total_percentage = 0
        self.total_alcohol = 0
        self.counter = 0
        self.elements = {}
        self.init_gui()

    def init_gui(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        drinks_frame = ctk.CTkFrame(master=self)
        drinks_frame.grid(row=0, column=0, sticky=ctk.NSEW,
                          padx=10, pady=10, columnspan=2)
        drinks_frame.grid_columnconfigure(0, weight=1)
        self.elements['drinks_frame'] = drinks_frame
        self.elements['add_button'] = ctk.CTkButton(
            master=self, command=self.add_drink)
        self.elements['add_button'].grid(
            row=1, column=0, sticky=ctk.EW, padx=10, pady=10)

        # TODO: improve info frame
        self.elements['info_frame'] = ctk.CTkFrame(master=self)
        self.elements['info_frame'].grid(
            row=1, column=1, sticky=ctk.EW, padx=10, pady=10)
        self.elements['total_volume_label'] = ctk.CTkLabel(
            master=self.elements['info_frame'], text='Total Volume: 0', justify=ctk.LEFT)
        self.elements['total_volume_label'].pack(pady=10)
        self.elements['total_percentage_label'] = ctk.CTkLabel(
            master=self.elements['info_frame'], text='Total Percentage: 0', justify=ctk.LEFT)
        self.elements['total_percentage_label'].pack(pady=10)

    def add_drink(self) -> None:
        current_drink = Drink(number=self.counter,
                              percentage=0, volume=0)
        # Add drink to dict
        self.drinks[f'Drink #{self.counter}'] = current_drink

        # Frame for drink
        drink_frame = ctk.CTkFrame(master=self.elements['drinks_frame'])
        drink_frame.grid(row=self.counter, column=0, sticky=ctk.NSEW)
        self.elements[f'drink_frame_{self.counter}'] = drink_frame

        # Text for volume
        self.create_slider_box(drink_frame, 'volume')
        self.create_slider_box(drink_frame, 'percentage')
        self.counter += 1

    def create_slider_box(self, parent_frame, feature) -> None:
        self.elements[f'{feature}_label_{self.counter}'] = ctk.CTkLabel(
            master=parent_frame, text=f'Drink #{self.counter} {feature}', justify=ctk.RIGHT)
        self.elements[f'{feature}_label_{self.counter}'].pack(
            pady=10, padx=10, anchor=ctk.W)

        # Box for slider and value
        slider_box = ctk.CTkFrame(master=parent_frame)
        slider_box.pack(pady=10, padx=10, fill=ctk.X)
        slider_box.grid_columnconfigure(0, weight=1)
        self.elements[f'{feature}_box_{self.counter}'] = slider_box

        # Slider and value
        if feature == 'volume':
            self.elements[f'{feature}_slider_{self.counter}'] = ctk.CTkSlider(
                master=slider_box,
                command=self.volume_slider_callback,
                number_of_steps=100, from_=0, to=400)
        else:
            self.elements[f'{feature}_slider_{self.counter}'] = ctk.CTkSlider(
                master=slider_box,
                command=self.percentage_slider_callback,
                number_of_steps=200, from_=0, to=100)
        self.elements[f'{feature}_slider_{self.counter}'].grid(
            row=0, column=0, sticky=ctk.W+ctk.E, padx=10, pady=10)
        self.elements[f'{feature}_value_{self.counter}'] = ctk.CTkLabel(
            master=slider_box, text=self.elements[f'{feature}_slider_{self.counter}'].get(), justify=ctk.RIGHT)
        self.elements[f'{feature}_value_{self.counter}'].grid(
            row=0, column=1, sticky=ctk.W+ctk.E, padx=10, pady=10)

    def volume_slider_callback(self, _) -> None:
        for i in range(self.counter):
            volume_value = self.elements[f'volume_slider_{i}'].get()
            self.drinks[f'Drink #{i}'].volume = volume_value
            self.elements[f'volume_value_{i}'].configure(text=volume_value)
        self.update_total()

    def percentage_slider_callback(self, _) -> None:
        for i in range(self.counter):
            percentage_value = self.elements[f'percentage_slider_{i}'].get()
            self.drinks[f'Drink #{i}'].percentage = percentage_value
            self.elements[f'percentage_value_{i}'].configure(
                text=percentage_value)
        self.update_total()

    def update_total(self) -> None:
        total_volume = 0
        total_alcohol = 0
        for drink in self.drinks.values():
            total_volume += drink.volume
            total_alcohol += drink.volume * (drink.percentage / 100)
        self.total_volume = total_volume
        self.total_alcohol = total_alcohol
        try:
            self.total_percentage = total_alcohol / total_volume * 100
        except ZeroDivisionError:
            self.total_percentage = 0
        self.update_gui()

    def update_gui(self):
        self.elements['total_volume_label'].configure(
            text=f"Total Volume: {self.total_volume}")
        self.elements['total_percentage_label'].configure(
            text=f"Total Percentage: {self.total_percentage:.2f}")


if __name__ == "__main__":
    app = DrinkCalculator()
    app.mainloop()
