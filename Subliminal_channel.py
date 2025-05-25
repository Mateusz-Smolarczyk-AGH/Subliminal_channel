import tkinter as tk
from tkinter import messagebox
import elgamal
import dsa

def process_texts_elgamal():
    text1 = entry1.get()
    text2 = entry2.get()
    podprogowa = elgamal.get_number_from_text(text1)
    message = elgamal.get_number_from_text(text2)
    public_key, private_key, signature = elgamal.elgamala_code(podprogowa, message)

    display_result(result_frame1, public_key)
    display_result(result_frame2, private_key)
    display_result(result_frame3, signature)

def process_texts_dsa():
    public_key_text = result_frame1.winfo_children()[0].get("1.0", tk.END).strip()
    private_key_text = result_frame2.winfo_children()[0].get("1.0", tk.END).strip()
    public_key = tuple(map(int, public_key_text.split()))
    private_key = int(private_key_text)
    text1 = entry1.get()
    text2 = entry2.get()
    if len(text1) > 16:
        messagebox.showinfo("Error", "Kanał podprogowy może mieć maksymalnie 16 znaków")

    podprogowa = elgamal.get_number_from_text(text1)
    message = elgamal.get_number_from_text(text2)
    signature = dsa.get_sign(private_key, public_key, message, podprogowa)
    display_result(result_frame3, signature)

def display_result(frame, result):
    for widget in frame.winfo_children():
        widget.destroy()
        
    text_display = tk.Text(frame, wrap=tk.WORD, height=5, width=50)
    text_display.insert(tk.END, result)
    text_display.grid(row=0, column=0, sticky="nsew")

    scrollbar = tk.Scrollbar(frame, command=text_display.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    text_display.config(yscrollcommand=scrollbar.set)

def check_signature_validity_elgamal():
    public_key_text = result_frame1.winfo_children()[0].get("1.0", tk.END).strip()
    signature_text = result_frame3.winfo_children()[0].get("1.0", tk.END).strip()
    message_text = entry2.get()

    public_key = tuple(map(int, public_key_text.split()))
    signature = tuple(map(int, signature_text.split()))
    message = elgamal.get_number_from_text(message_text)

    valid = elgamal.check_signature(public_key, signature, message)
    messagebox.showinfo("Weryfikacja podpisu", "Podpis jest poprawny" if valid else "Podpis jest niepoprawny")

def check_signature_validity_dsa():
    public_key_text = result_frame1.winfo_children()[0].get("1.0", tk.END).strip()
    signature_text = result_frame3.winfo_children()[0].get("1.0", tk.END).strip()
    message_text = entry2.get()

    public_key = tuple(map(int, public_key_text.split()))
    signature = tuple(map(int, signature_text.split()))
    message = elgamal.get_number_from_text(message_text)

    valid = dsa.verify(signature, public_key, message)
    messagebox.showinfo("Weryfikacja podpisu", "Podpis jest poprawny" if valid else "Podpis jest niepoprawny")

def get_subliminal_message_elgamal():
    public_key_text = result_frame1.winfo_children()[0].get("1.0", tk.END).strip()
    private_key_text = result_frame2.winfo_children()[0].get("1.0", tk.END).strip()
    signature_text = result_frame3.winfo_children()[0].get("1.0", tk.END).strip()
    message_text = entry2.get()
    message = elgamal.get_number_from_text(message_text)

    public_key = tuple(map(int, public_key_text.split()))
    private_key = int(private_key_text)
    signature = tuple(map(int, signature_text.split()))

    subliminal_message = elgamal.get_subliminal_channel(public_key, private_key, signature, message)
    messagebox.showinfo("Podprogowy przekaz", f"Podprogowy przekaz: {subliminal_message}")

def get_subliminal_message_dsa():
    public_key_text = result_frame1.winfo_children()[0].get("1.0", tk.END).strip()
    private_key_text = result_frame2.winfo_children()[0].get("1.0", tk.END).strip()
    signature_text = result_frame3.winfo_children()[0].get("1.0", tk.END).strip()
    message_text = entry2.get()
    message = elgamal.get_number_from_text(message_text)

    public_key = tuple(map(int, public_key_text.split()))
    private_key = int(private_key_text)
    signature = tuple(map(int, signature_text.split()))

    subliminal_message = dsa.get_subominal(signature, public_key, message, private_key)
    messagebox.showinfo("Podprogowy przekaz", f"Podprogowy przekaz: {subliminal_message}")

def generate_keys_dsa():
    private_key, public_key = dsa.get_keys()
    display_result(result_frame1, public_key)
    display_result(result_frame2, private_key)

def set_algorithm(algorithm):
    global current_algorithm
    current_algorithm = algorithm
    algorithm_label.config(text=f"Algorytm: {algorithm}")
    if algorithm == "ElGamal":
        process_button.config(command=process_texts_elgamal, text="Wygeneruj klucze i podpis")
        check_signature_button.config(command=check_signature_validity_elgamal)
        get_subliminal_message_button.config(command=get_subliminal_message_elgamal)
        generate_keys_button.grid_remove()
    elif algorithm == "DSA":
        process_button.config(command=process_texts_dsa, text="Wygeneruj podpis")
        check_signature_button.config(command=check_signature_validity_dsa)
        get_subliminal_message_button.config(command=get_subliminal_message_dsa)
        generate_keys_button.grid(row=1, column=0, padx=10, pady=5, sticky="e")

def show_help():
    if current_algorithm == "ElGamal":
        messagebox.showinfo("Pomoc", "Ta aplikacja ma na celu zademonstrować wykorzystanie kanału podprogowego zaimplementowanego w algorytmie Elgamal"+
                            "\n\nInstrukcja obsługi:\n\n1. Wypełnij pola zawierające wiadomość niewinną i podprogową.\n\n"+
                            "2. Naciśnij przycisk Wygeneruj klucze i podpis - na podstawie wpisanych wiadomości wygeneruje on klucz publiczny, klucz prywatny oraz podpis cyfrowy. "+
                            "Uzyskane wyniki zostaną wyświetlone poniżej. Można je edytować lub wkleić własne." +
                            "\n\n3. Można sprawdzić poprawność podpisu za pomocą przycisku Sprawdź poprawność podpisu. Bierze on wartości z pól aplikacji, więc jeżeli zostaną zmienione, zostanie to uwzględnione. "+
                            "(udowadnia to, że rzeczywiście sprawdzane są wyniki, a zwracana wartość nie jest z góry przypisana)"+
                            "\n\n4. Można odczytać kanał podprogowy za pomocą przycisku Uzyskaj podprogowy przekaz")
    elif current_algorithm == "DSA":
        messagebox.showinfo("Pomoc", "Ta aplikacja ma na celu zademonstrować wykorzystanie kanału podprogowego zaimplementowanego w algorytmie DSA"+
                            "\n\nInstrukcja obsługi:\n\n1. Naciśnij przycisk wygeneruj klucze, aby wygenerować klucz publiczny i prywatny"+
                            ". Ten krok nie wymaga podania wiadomości. \n\n2. Wypełnij pola zawierające wiadomość niewinną i podprogową. Wiadomość podprogowa może mieć maksymalnie 16 znaków.\n\n"+
                            "3. Naciśnij przycisk Wygeneruj podpis - na podstawie wpisanych wiadomości wygeneruje on podpis cyfrowy. "+
                            "Uzyskane wyniki zostaną wyświetlone poniżej. Można je edytować lub wkleić własne." +
                            "\n\n4. Można sprawdzić poprawność podpisu za pomocą przycisku Sprawdź poprawność podpisu. Bierze on wartości z pól aplikacji, więc jeżeli zostaną zmienione, zostanie to uwzględnione."+
                            "(udowadnia to, że rzeczywiście sprawdzane są wyniki, a zwracana wartość nie jest z góry przypisana)"+
                            "\n\n5. Można odczytać kanał podprogowy za pomocą przycisku Uzyskaj podprogowy przekaz")

def show_theory():
    if current_algorithm == "ElGamal":
        theory_text = (
        "Algorytm ElGamala podpisu cyfrowego z kanałem podprogowym:\n\n"
        "I. Generowanie kluczy podobnie jak w podstawowym algorytmie ElGamala:\n\n"
        "1) Wybierana jest liczba pierwsza p.\n"
        "2) Wybierana jest liczba losowa g i r mniejsze od p.\n"
        "3) Oblicza się k = g^r mod p.\n"
        "4) Klucz jawny stanowią liczby k, g i p (k służy do sprawdzania podpisu).\n"
        "5) Klucz prywatny to liczba r. Klucz prywatny r znają Alice i Bob, ten klucz służy do odczytania wiadomości podprogowej oraz do podpisu wiadomości wyglądającej niewinnie.\n\n"
        "II. Przesyłanie wiadomości podprogowej M z wykorzystaniem wiadomości niewinnej M':\n\n"
        "1) Należy zagwarantować, aby M i p były względnie pierwsze oraz by M i p - 1 były względnie pierwsze.\n"
        "2) Alice wyznacza podpis X i w tym celu oblicza X = g^M mod p, M jest wiadomością podprogową i ona służy jako tajny klucz szyfrowania.\n"
        "3) Alice rozwiązując algorytmem Euklidesa następujące równanie w celu wyznaczenia Y\n\n"
        "M' = rX + MY (mod p - 1)\n\n"
        "gdzie: M' - wiadomość podpisywana, M - wiadomość podprogowa.\n"
        "4) Podpis Alice to para X i Y.\n\n"
        "III. Weryfikacja podpisu i odczytywanie informacji podprogowej:\n\n"
        "1) Strażnik przechwytujący wiadomość może sprawdzić ważność podpisu przez sprawdzenie równania\n\n"
        "k^X * X^Y mod p = g^M' mod p.\n"
        "2) W celu odtworzenia wiadomości podprogowej M Bob oblicza jej wartość z równania\n\n"
        "M = Y^(-1)(M' - rX) mod p - 1.\n\n\n"
        "Źródło: Marek R. Ogiela, Podstawy Kryptografii, Kraków 2000"
        )
        messagebox.showinfo("Teoria - Podpisywanie i weryfikacja w DSA", theory_text)
    elif current_algorithm == "DSA":
        theory_text = (
        "Generowanie kluczy w DSA\n\n"
        "Każdy z uczestników protokołu, w którym wykorzystuje się algorytm DSA, wykonuje następujące kroki:\n\n"
        "1. Wybieranie liczby pierwszej q takiej, że 2^159 < q < 2^160 (najmniejszy pierwszy o długości 160 bitów liczby p - 1 z punktu 2).\n"
        "2. Wybieranie liczby pierwszej p z zakresu 2^511+64k < p < 2^512+64k takiej, że q dzieli p - 1. Liczba k przyjmuje wartości z zakresu {0, 1, ..., 8} "
        "(oznacza to, że p ma długość od 512 do 1024 bitów, która jest wielokrotnością 64).\n"
        "3. Obliczanie g = h^(p-1)/q mod p, gdzie h jest dowolną liczbą mniejszą od p - 1, ale taką, że wyrażenie h^(p-1)/q mod p jest większe od 1.\n"
        "4. Wybieranie losowo liczby x (o długości 160 bitów) mniejszej od q.\n"
        "5. Obliczanie y = g^x mod p.\n"
        "6. Parametry p, q, g i y są jawne i mogą być używane wspólnie przez pewną grupę użytkowników (wchodzą w skład klucza jawnego). Liczba x jest kluczem prywatnym. Liczba y jest kluczem jawnym.\n\n"
        "W trakcie generowania podpisu algorytm DSA wykorzystuje jednokierunkową funkcję haszującą H(m). W przypadku DSA funkcja ta jest określona przez funkcję skrótu SHA-256\n\n"
        "Podpisywanie i weryfikacja w DSA\n\n"
        "Załóżmy, że Alice chce podpisać binarną wiadomość m o dowolnej długości i przesłać ją do Boba. Bob chce zweryfikować podpis używając klucza publicznego Alice. "
        "W tym celu oboje realizują następujące kroki:\n\n"
        "I. Generowanie podpisu przez Alice (gdy już wygenerowane klucze jawny i tajny):\n\n"
        "1. k to wiadomość podprogowa. Musi być mniejsza niż q.\n"
        "2. Obliczana jest pierwsza część podpisu r = (g^k mod p) mod q.\n"
        "3. Obliczana jest s = k^(-1)(H(m) + x * r) mod q.\n"
        "4. Podpis wiadomości m stanowi para (r, s).\n\n"
        "II. Weryfikacja podpisu przez Boba:\n\n"
        "1. Obliczana jest liczba w = s^(-1) mod q.\n"
        "2. Obliczane są wartości u1 = (H(m) * w) mod q oraz u2 = (r * w) mod q.\n"
        "3. Obliczana jest v = (g^u1 * y^u2 mod p) mod q.\n"
        "4. Podpis jest poprawny wtedy i tylko wtedy, gdy v = r.\n\n"
        "III. Kanał podprogowy:\n\n"
        "Kanał podprogowy jest wyliczany za pomacą następującego wzoru\n\n"
        "m' ≡ s^(-1)(h + xr) mod q.\n\n\n"
        "Źródło: Marek R. Ogiela, Podstawy Kryptografii, Kraków 2000"
    )
    messagebox.showinfo("Teoria - Podpisywanie i weryfikacja w DSA", theory_text)

# Utwórz główne okno aplikacji
root = tk.Tk()
root.title("Kanał Podprogowy z ElGamal i DSA")

# Ustawienie rozmiaru okna na 1000x600 pikseli
root.geometry("600x600")

# Konfiguracja kolumn
root.grid_columnconfigure(0, weight=1)

# Menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
algorithm_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Wybierz Algorytm", menu=algorithm_menu)
algorithm_menu.add_command(label="ElGamal", command=lambda: set_algorithm("ElGamal"))
algorithm_menu.add_command(label="DSA", command=lambda: set_algorithm("DSA"))

# Dodanie etykiety wyświetlającej aktualnie używany algorytm
algorithm_label = tk.Label(root, text="Algorytm ElGamal", font=("Helvetica", 16))
algorithm_label.grid(row=0, column=0, padx=10, pady=5, sticky="n")

# Dodanie przycisków "Pomoc" i "Teoria"
help_button = tk.Button(root, text="Pomoc", command=show_help, bg="gray", fg="#fff")
help_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")

theory_button = tk.Button(root, text="Teoria", command=show_theory, bg="gray", fg="#fff")
theory_button.grid(row=0, column=0, padx=10, pady=5, sticky="e")

# Utwórz widgety
label1 = tk.Label(root, text="Wpisz wiadomość podprogową:")
label1.grid(row=1, column=0, padx=10, pady=5, sticky="ws")

entry1 = tk.Entry(root, width=50)
entry1.grid(row=2, column=0, padx=10, pady=5, sticky="wn")

label2 = tk.Label(root, text="Wpisz wiadomość:")
label2.grid(row=3, column=0, padx=10, pady=5, sticky="ws")

entry2 = tk.Entry(root, width=50)
entry2.grid(row=4, column=0, padx=10, pady=5, sticky="wn")

label3 = tk.Label(root, text="Wpisz wiadomość podprogową:")
label3.grid(row=5, column=0, padx=10, pady=5, sticky="ws")
label3.grid_remove()

entry3 = tk.Entry(root, width=50)
entry3.grid(row=6, column=0, padx=10, pady=5, sticky="wn")
entry3.grid_remove()

generate_keys_button = tk.Button(root, text="Generuj Klucze DSA", command=generate_keys_dsa, bg="gray", fg="#fff")

process_button = tk.Button(root, text="Wygeneruj podpis", command=process_texts_elgamal, bg="gray", fg="#fff")
process_button.grid(row=2, column=0, padx=10, pady=10, sticky="e")

result_frame1 = tk.LabelFrame(root, text="Klucz publiczny", padx=10, pady=10)
result_frame1.grid(row=8, column=0, padx=10, pady=10, sticky="nsew")

result_frame2 = tk.LabelFrame(root, text="Klucz prywatny", padx=10, pady=10)
result_frame2.grid(row=9, column=0, padx=10, pady=10, sticky="nsew")

result_frame3 = tk.LabelFrame(root, text="Podpis cyfrowy", padx=10, pady=10)
result_frame3.grid(row=10, column=0, padx=10, pady=10, sticky="nsew")

check_signature_button = tk.Button(root, text="Sprawdź poprawność podpisu", command=check_signature_validity_elgamal, bg="gray", fg="#fff")
check_signature_button.grid(row=3, column=0, padx=10, pady=10, sticky="e")

get_subliminal_message_button = tk.Button(root, text="Uzyskaj podprogowy przekaz", command=get_subliminal_message_elgamal, bg="gray", fg="#fff")
get_subliminal_message_button.grid(row=4, column=0, padx=10, pady=10, sticky="e")

# Konfiguracja wierszy
for i in range(13):
    root.grid_rowconfigure(i, weight=1)

# Ustaw algorytm domyślny
current_algorithm = "ElGamal"
set_algorithm(current_algorithm)

# Uruchom główną pętlę aplikacji
root.mainloop()
