import tkinter
import mainfuncs
from tkinter import messagebox


def calculate_boton():
    exo_rad = float(entrada1.get())
    star_type = entrada2.get().upper()
    exo_type = entrada3.get()
    exo_orbit = float(entrada4.get()) * 149597870700
    star_rad = float(entrada5.get()) * 6.957 * 10 ** 8
    x = True
    result = mainfuncs.calculate_IST(exo_rad, exo_type, star_type, exo_orbit, star_rad, x)
    if result.is_habitable:
        habitable_text = "Està a dins de la zona habitable"
    else:
        habitable_text = "No està a dins de la zona habitable"
    messagebox.showinfo("IST", "L'IST de l'exoplaneta és d'un " + result.ist + "%\n" + "La seva temperatura són ")


def place_all(*widgets):
    i = 1
    for widget in widgets:
        widget.place(x=450, y=30 + i*30)
        i += 1


main_window = tkinter.Tk()
main_window.geometry("900x600")
boton = tkinter.Button(main_window, text="calculate IST", command=calculate_boton, underline="0", width=10, bd=20,
                       bg="purple")
entrada1, entrada2, entrada3, entrada4, entrada5 = tkinter.Entry(main_window, width=20), \
                                                   tkinter.Entry(main_window, width=20), \
                                                   tkinter.Entry(main_window, width=20), \
                                                   tkinter.Entry(main_window, width=20), \
                                                   tkinter.Entry(main_window, width=20)
label1 = tkinter.Label(main_window, text="Radi de l'exoplaneta:")
place_all(entrada1, entrada2, entrada3, entrada4, entrada5, boton)
label1.place(x=300, y = 60)
entrada1.insert(0, "0.091")
entrada2.insert(0, "k")
entrada3.insert(0, "Terra")
entrada4.insert(0, "1")
entrada5.insert(0, "1")
main_window.mainloop()
