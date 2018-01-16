import mainfuncs
from tkinter import messagebox
from tkinter import *
import textwrap


class HoverText:
    def __init__(self, app, text):
        if len(text) < 20:
            width = len(text) * 6
        else:
            width = 20 * 6
        text = textwrap.wrap(text, 20)
        height = len(text) * 20
        text = "\n".join(text)
        self.canvas = Canvas(app.master, height=height, width=width, bg="old lace", highlightbackground="grey")
        self.cordx = app.master.winfo_pointerx() - app.master.winfo_rootx()
        self.cordy = app.master.winfo_pointery() - app.master.winfo_rooty()
        self.canvas.place(x=self.cordx + 5, y=self.cordy + 5)
        self.canvas.create_text(width / 2, height / 2, text=text)


class Exocalc:
    def __init__(self, master):
        self.master = master
        self.master.title("Exocalc")
        self.master.geometry("700x400")
        self.master.resizable(width=False, height=False)

        self.now_hovering = None
        self.result = None
        self.current_text = StringVar(self.master, textwrap.fill("Benvingut! La informació es mostrarà aquí. Pots arrossegar el ratolí per sobre del nom de cada apartat per obtenir més informació.", 39))
        self.current_text.trace("w", self.update_text)
        self.habitable_texts = ["El planeta és a la zona habitable", "El planeta no és a la zona habitable"]
        self.habitable_text = StringVar(self.master, "")
        self.options_albedo = ["Terra", "Neptú", "Júpiter"]
        self.options_star_type = ["O (35.000 K)", "B (15.000 K)", "A (9.000 K)", "F (7.000 K)", "G (5.500 K)", "K (4000 K)", "M (3000 K)", "SOL (5772 K)"]

        self.men = Menu(self.master)
        self.men.add_command(label="Informació", command=self.show_info)
        self.men.add_command(label="Sobre...", command=self.show_about)
        self.men.add_command(label="Sortir", command=self.master.quit)
        self.master.config(menu=self.men)

        self.albedo_variable = StringVar(self.master, self.options_albedo[0])
        self.albedo_menu = OptionMenu(self.master, self.albedo_variable, *self.options_albedo)
        self.albedo_menu.config(width=13)

        self.star_type_variable = StringVar(self.master, self.options_star_type[0])
        self.star_type_menu = OptionMenu(self.master, self.star_type_variable, *self.options_star_type)
        self.star_type_menu.config(width=13)

        self.input_radius = Entry(self.master, width=20)
        self.input_exo_orbit = Entry(self.master, width=20)
        self.input_star_radius = Entry(self.master, width=20)
        self.button = Button(self.master, text="Calcular IST", command=self.calculate, bg="SkyBlue")

        self.radius_label = Label(self.master, text="Radi de l'exoplaneta:", width=25, anchor="e")
        self.star_type_label = Label(self.master, text="Tipus d'estrella:", width=25, anchor="e")
        self.albedo_label = Label(self.master, text="Albedo del tipus:", width=25, anchor="e")
        self.orbit_label = Label(self.master, text="Radi òrbita de l'exoplaneta:", width=25, anchor="e")
        self.star_radius_label = Label(self.master, text="Radi de la estrella:", width=25, anchor="e")
        self.habitable_label = Label(self.master, width=26, textvariable=self.habitable_text, anchor="center")

        self.status_canvas = Canvas(self.master, height=350, width=240, bg="white", highlightbackground="gainsboro")
        self.status_text = self.status_canvas.create_text(10, 10, text=self.current_text.get(), anchor="nw")

        self.status_canvas.place(x=420, y=15)
        self.place_all(250, 30, 40, self.input_radius, self.star_type_menu, self.albedo_menu, self.input_exo_orbit, self.input_star_radius,
                       self.button)
        self.place_all(50, 30, 40, self.radius_label, self.star_type_label, self.albedo_label, self.orbit_label,
                       self.star_radius_label)
        self.habitable_label.place(x=210, y=300)

        self.radius_label.bind("<Enter>", lambda x: self.show_text(x, "Radi de l'exoplaneta, en Radis de Júpiter."))
        self.radius_label.bind("<Leave>", self.hide_text)
        self.star_type_label.bind("<Enter>", lambda x: self.show_text(x, "Tipus d'estrella que orbita l'exoplaneta en funció de la temperatura."))
        self.star_type_label.bind("<Leave>", self.hide_text)
        self.albedo_label.bind("<Enter>", lambda x: self.show_text(x, "Planeta amb albedo més proper al de l'exoplaneta."))
        self.albedo_label.bind("<Leave>", self.hide_text)
        self.orbit_label.bind("<Enter>", lambda x: self.show_text(x, "Distància mitja de l'exoplaneta a l'estrella, en UA."))
        self.orbit_label.bind("<Leave>", self.hide_text)
        self.star_radius_label.bind("<Enter>", lambda x: self.show_text(x, "Radi de l'estrella que orbita l'exoplaneta, en Radis Solars."))
        self.star_radius_label.bind("<Leave>", self.hide_text)

        self.master.mainloop()

    def calculate(self):
        width = 39
        jump = "\n\n"
        result_message = ""
        error = False
        try:
            exo_rad = float(self.input_radius.get().replace(",", "."))
        except ValueError:
            result_message += textwrap.fill("El radi de l'exoplaneta ha de ser un número vàlid!", width) + jump
            error = True
        star_type = self.star_type_variable.get()
        exo_type = self.albedo_variable.get()
        try:
            exo_orbit = float(self.input_exo_orbit.get().replace(",", ".")) * 149597870700
        except ValueError:
            result_message += textwrap.fill("L'òrbita de l'exoplaneta ha de ser un número vàlid!", width) + jump
            error = True
        try:
            star_rad = float(self.input_star_radius.get().replace(",", ".")) * 6.957 * 10 ** 8
        except ValueError:
            result_message += textwrap.fill("El radi de l'estrella ha de ser un número vàlid!", width) + jump
            error = True
        if error is True:
            self.current_text.set(result_message)
            self.habitable_text.set("")
            return
        result = mainfuncs.calculate_IST(exo_rad, exo_type, star_type, exo_orbit, star_rad)
        result_message += textwrap.fill("Aquests són els resultats:", width) + jump
        result_message += textwrap.fill("L'IST de l'exoplaneta és d'un " + str(result.ist) + "%", width) + jump
        result_message += textwrap.fill("El seu radi mesura " + str(result.radius) + " Rj, amb una semblança a la Terra del " + str(result.radius_relation) + "%", width) + jump
        result_message += textwrap.fill("La seva densitat és de " + str(result.density) + " kg/m^3, amb una semblança a la Terra del " + str(result.density_relation) + "%", width) + jump
        result_message += textwrap.fill("La seva velocitat d'escapament és de " + str(result.escape_velocity) + " m/s, amb una semblança a la Terra del " + str(result.escape_velocity_relation) + "%", width) + jump
        result_message += textwrap.fill("La seva temperatura és de " + str(result.temperature) + " K, amb una semblança a la Terra del " + str(result.temperature_relation) + "%", width) + jump
        self.current_text.set(result_message)
        if result.is_habitable:
            self.habitable_text.set(self.habitable_texts[0])
            self.habitable_label.config(fg="green")
        else:
            self.habitable_text.set(self.habitable_texts[1])
            self.habitable_label.config(fg="red")

    def show_text(self, event, text):
        self.now_hovering = HoverText(self, text)

    def hide_text(self, event):
        self.now_hovering.canvas.destroy()
        del self.now_hovering

    def update_text(self, *args):
        self.status_canvas.itemconfigure(self.status_text, text=self.current_text.get())

    @staticmethod
    def place_all(x_position, y_position, y_variation, *widgets):
        for i in range(len(widgets)):
            if isinstance(widgets[i], Button):
                tempx = 23
                tempy = 0
            elif isinstance(widgets[i], OptionMenu):
                tempx = 0
                tempy = -7
            else:
                tempx = 0
                tempy = 0
            widgets[i].place(x=x_position + tempx, y=y_position + tempy + i * y_variation)

    @staticmethod
    def show_info():
        messagebox.showinfo("Informació", "Els càlculs realitzats en aquest programa en relació a la temperatura no tenen en compte factors atmosfèrics, com l'efecte hivernacle, ni factors geològics, com l'activitat volcànica.")

    @staticmethod
    def show_about():
        messagebox.showinfo("Sobre...", "Exocalc V1.0\nContacte: (email)\n")


garik = Exocalc(Tk())
