from PIL import Image, ImageTk
import tkinter as tk
from tkinter.ttk import Combobox
import csv
from tkinter import messagebox
from tkinter import Toplevel, ttk 
import re 
from tkinter import simpledialog
from tkinter import filedialog
import random  
import os  
import hashlib
root = tk.Tk()  
root.geometry('500x600')
root.title('Student Management')

bg_color = '#1B6165'
ADMIN_FILE = "admins.csv"
def load_resized_image(path, size=(55, 50)):
    img = Image.open(path)
    img = img.resize(size, Image.Resampling.LANCZOS)  # Compatible Pillow >= 10
    return ImageTk.PhotoImage(img)

def forward_to_welcome_page():
    for widget in root.winfo_children():
        widget.destroy()
    welcome_page()


login_student_icon = load_resized_image('student.png')
login_admin_icon = load_resized_image('settings.png')
add_student_icon = load_resized_image('add.png')
locked_icon = load_resized_image('locked.png', size=(30, 30))
unlocked_icon = load_resized_image('unlocked.png', size=(30, 30))
add_student_pic_icon = load_resized_image('add.png', size=(100, 100))


if not os.path.exists(ADMIN_FILE):
    with open(ADMIN_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Nom", "MotDePasse"])
        writer.writerow(["0001", "Aissam", "aissam@123"])
        writer.writerow(["0002", "Nassima", "nassima@123"])

def import_data():
    file_path = filedialog.askopenfilename(
        title="Importer un fichier CSV", filetypes=[("Fichiers CSV", "*.csv")]
    )
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # sauter l'en-tête
                data = list(reader)
            messagebox.showinfo("Importation réussie", f"{len(data)} lignes importées avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'importation : {e}")
def export_data():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv")],
        title="Exporter les données"
    )
    if file_path:
        try:
            with open("etudiants.csv", 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                data = list(reader)
            with open(file_path, 'w', newline='', encoding='utf-8') as f_out:
                writer = csv.writer(f_out)
                writer.writerows(data)
            messagebox.showinfo("Exportation réussie", "Données exportées avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'exportation : {e}")
def delete_student():
    student_id_to_delete = simpledialog.askstring("Supprimer Étudiant", "Entrez l'ID de l'étudiant à supprimer :")
    if not student_id_to_delete:
        return

    try:
        with open("etudiants.csv", 'r', encoding='utf-8') as f:
            lines = list(csv.reader(f))

        header = lines[0]
        data = lines[1:]
        new_data = [row for row in data if row[0] != student_id_to_delete]

        if len(data) == len(new_data):
            messagebox.showinfo("Info", "Aucun étudiant trouvé avec cet ID.")
            return

        with open("etudiants.csv", 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(new_data)

        messagebox.showinfo("Succès", f"Étudiant avec ID {student_id_to_delete} supprimé.")
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Fichier etudiants.csv introuvable.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur : {e}")
def afficher_etudiants():
    try:
        with open("etudiants.csv", "r", encoding="utf-8") as f:
            data = list(csv.reader(f))
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Fichier etudiants.csv introuvable.")
        return

    if len(data) < 2:
        messagebox.showinfo("Information", "Aucun étudiant inscrit.")
        return

    window = tk.Toplevel()
    window.title("Liste des étudiants")
    window.geometry("800x400")

    table = ttk.Treeview(window, columns=data[0], show='headings')
    table.pack(expand=True, fill='both')

    for col in data[0]:
        table.heading(col, text=col)
        table.column(col, anchor=tk.CENTER)

    for row in data[1:]:
        table.insert("", tk.END, values=row)

def welcome_page():

    def forward_to_student_login_page():
        welcome_page_fm.destroy()
        root.update()
        student_login_page()

    def forward_to_admin_login_page():
        welcome_page_fm.destroy()
        root.update()
        admin_login_page()

    def forward_to_add_account_page():
        welcome_page_fm.destroy()
        root.update()
        add_account_page()

    # Cadre principal
    welcome_page_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)
    welcome_page_fm.pack(pady=30)
    welcome_page_fm.pack_propagate(False)
    welcome_page_fm.configure(width=400, height=420)

    # Titre
    heading_lb = tk.Label(
        welcome_page_fm,
        text="Bienvenue à l'inscription \n des étudiants",
        bg=bg_color,
        fg='white',
        font=('Helvetica', 18, 'bold')
    )
    heading_lb.place(x=0, y=0, width=400)

    # Login Student
    student_login_img = tk.Label(welcome_page_fm, image=login_student_icon, bd=0, bg='white',)
    student_login_img.place(x=60, y=100)

    login_student_btn = tk.Button(welcome_page_fm, text='Login Student', bg=bg_color,
                                fg='white', font=('Bold', 15), bd=0,
                                command=forward_to_student_login_page)
    login_student_btn.place(x=120, y=110, width=200)

    # Login Admin
    admin_login_img = tk.Label(welcome_page_fm, image=login_admin_icon, bd=0, bg='white')
    admin_login_img.place(x=60, y=170)

    admin_login_btn = tk.Button(welcome_page_fm, text='Login Admin', bg=bg_color,
                                fg='white', font=('Bold', 15), bd=0,
                                command=forward_to_admin_login_page)
    admin_login_btn.place(x=120, y=180, width=200)

    # Add Student
    add_student_img = tk.Label(welcome_page_fm, image=add_student_icon, bd=0, bg='white')
    add_student_img.place(x=60, y=240)

    add_student_btn = tk.Button(welcome_page_fm, text='Créer un compte', bg=bg_color,
                                fg='white', font=('Bold', 15), bd=0,
                                command=forward_to_add_account_page)
    add_student_btn.place(x=120, y=250, width=200)
    
        # Bouton Quitter
    quit_btn = tk.Button(
        welcome_page_fm,
        text='Quitter',
        bg='red',
        fg='white',
        font=('Bold', 15),
        bd=0,
        command=root.quit  # Ferme l'application
    )
    quit_btn.place(x=120, y=310, width=200)

def student_login_page():
    def show_hide_password():
        if password_ent['show'] == '*':
            password_ent.config(show='')
            show_hide_btn.config(image=unlocked_icon)
        else:
            password_ent.config(show='*')
            show_hide_btn.config(image=locked_icon)

    def forward_to_welcome_page():
        student_login_page_fm.destroy()
        root.update()
        welcome_page()

    def login_student():
        entered_id = id_number_ent.get().strip()
        entered_password = password_ent.get().strip()

        try:
            with open("etudiants.csv", "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader, None)  # Ignore header if exists
                for row in reader:
                    hashed_input_password = hashlib.sha256(entered_password.encode()).hexdigest()
                    if len(row) >= 8 and row[0] == entered_id and row[7] == hashed_input_password:
                        messagebox.showinfo("Succès", "Connexion réussie!")
                        return
                messagebox.showerror("Erreur", "ID ou mot de passe incorrect!")
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Fichier etudiants.csv introuvable.")

    def recover_password():
        email = simpledialog.askstring("Récupération", "Entrez votre email:")
        if not email:
            return
        try:
            with open("etudiants.csv", "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 7 and row[6] == email:
                        messagebox.showinfo("Mot de passe retrouvé", f"Votre mot de passe est : {row[7]}")
                        return
                messagebox.showerror("Erreur", "Email non trouvé.")
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Fichier etudiants.csv introuvable.")

    student_login_page_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)

    heading_lb = tk.Label(student_login_page_fm,
                          text="Bienvenue à l'inscription \n des étudiants",
                          bg=bg_color, fg='white', font=('Helvetica', 18, 'bold'))
    heading_lb.place(x=0, y=0, width=400)

    back_btn = tk.Button(student_login_page_fm, text='←', font=('bold', 20), fg=bg_color, bd=0,
                         command=forward_to_welcome_page)
    back_btn.place(x=5, y=40)

    stud_icon_lb = tk.Label(student_login_page_fm, image=login_student_icon)
    stud_icon_lb.place(x=170, y=80)

    id_number_lb = tk.Label(student_login_page_fm, text="Entrez le numéro d'identification étudiant:",
                            font=('bold', 15), fg=bg_color)
    id_number_lb.place(x=30, y=130)

    id_number_ent = tk.Entry(student_login_page_fm, font=('bold', 15),
                             justify=tk.CENTER, highlightcolor=bg_color,
                             highlightbackground='gray', highlightthickness=2)
    id_number_ent.place(x=80, y=170)

    password_lb = tk.Label(student_login_page_fm, text="Entrez le mot de passe étudiant:",
                           font=('bold', 15), fg=bg_color)
    password_lb.place(x=50, y=220)

    password_ent = tk.Entry(student_login_page_fm, font=('bold', 15),
                            justify=tk.CENTER, highlightcolor=bg_color,
                            highlightbackground='gray', highlightthickness=2,
                            show='*')
    password_ent.place(x=80, y=260)

    show_hide_btn = tk.Button(student_login_page_fm, image=locked_icon, bd=0,
                              command=show_hide_password)
    show_hide_btn.place(x=310, y=260)

    login_btn = tk.Button(student_login_page_fm, text='Login',
                          font=('Bold', 15), bg=bg_color, fg='white',
                          command=login_student)
    login_btn.place(x=95, y=310, width=200, height=40)

    forget_password_btn = tk.Button(student_login_page_fm, text='⚠\nMot de passe oublié',
                                    fg=bg_color, bd=0, command=recover_password)
    forget_password_btn.place(x=140, y=370)

    student_login_page_fm.pack(pady=30)
    student_login_page_fm.pack_propagate(False)
    student_login_page_fm.configure(width=400, height=450)

def admin_login_page():
    def show_hide_password():
        if password_ent['show'] == '*':
            password_ent.config(show='')
            show_hide_btn.config(image=unlocked_icon)
        else:
            password_ent.config(show='*')
            show_hide_btn.config(image=locked_icon)

    def forward_to_welcome_page():
        admin_login_page_fm.destroy()
        root.update()
        welcome_page()

    def admin_login():
        admin_id = id_number_ent.get()
        password = password_ent.get()
        try:
            with open("admins.csv", 'r', encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if row[0] == admin_id and row[2] == password:
                        messagebox.showinfo("Succès", f"Bonjour {row[1]}!")
                        admin_login_page_fm.destroy()  # Ferme la page de login
                        admin_access_page()            # Affiche la page admin
                        return
                messagebox.showerror("Erreur", "Identifiants admin incorrects!")
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Fichier des administrateurs introuvable.")

    admin_login_page_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)

    heading_lb = tk.Label(admin_login_page_fm, text='Admin Login Page',
                          font=('bold', 20), bg=bg_color, fg='white')
    heading_lb.place(x=0, y=0, width=400)

    back_btn = tk.Button(admin_login_page_fm, text='←', font=('bold', 20), fg=bg_color, bd=0,
                         command=forward_to_welcome_page)
    back_btn.place(x=5, y=40)

    admin_icon_lb = tk.Label(admin_login_page_fm, image=login_admin_icon)
    admin_icon_lb.place(x=165, y=60)

    id_number_lb = tk.Label(admin_login_page_fm, text='Enterez le numéro d\'identification\nadmin:',
                            font=('bold', 15), fg=bg_color)
    id_number_lb.place(x=60, y=130)

    id_number_ent = tk.Entry(admin_login_page_fm, font=('bold', 15),
                             justify=tk.CENTER, highlightcolor=bg_color,
                             highlightbackground='gray', highlightthickness=2)
    id_number_ent.place(x=80, y=190)

    password_lb = tk.Label(admin_login_page_fm, text='Enterez le mot de passe\nadmin :',
                           font=('bold', 15), fg=bg_color)
    password_lb.place(x=85, y=240)

    password_ent = tk.Entry(admin_login_page_fm, font=('bold', 15),
                            justify=tk.CENTER, highlightcolor=bg_color,
                            highlightbackground='gray', highlightthickness=2,
                            show='*')
    password_ent.place(x=80, y=290)

    show_hide_btn = tk.Button(admin_login_page_fm, image=locked_icon, bd=0,
                              command=show_hide_password)
    show_hide_btn.place(x=310, y=290)

    login_btn = tk.Button(admin_login_page_fm, text='Login',
                          font=('Bold', 15), bg=bg_color, fg='white',
                          command=admin_login)
    login_btn.place(x=95, y=340, width=200, height=40)

    admin_login_page_fm.pack(pady=30)
    admin_login_page_fm.pack_propagate(False)
    admin_login_page_fm.configure(width=400, height=540)

def admin_access_page():
    admin_page_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)
    
    heading_lb = tk.Label(admin_page_fm, text='Admin Access Page',
                          font=('bold', 20), bg=bg_color, fg='white')
    heading_lb.place(x=0, y=0, width=400)

    # Boutons avec style uniforme
    import_btn = tk.Button(admin_page_fm, text='Importer CSV',
                           font=('Bold', 10), bg='white', fg=bg_color,
                           command=import_data)
    import_btn.place(x=40, y=100, width=140)

    export_btn = tk.Button(admin_page_fm, text='Exporter CSV',
                           font=('Bold', 10), bg='white', fg=bg_color,
                           command=export_data)
    export_btn.place(x=220, y=100, width=140)

    delete_btn = tk.Button(admin_page_fm, text='Supprimer Étudiant',
                           font=('Bold', 10), bg='white', fg=bg_color,
                           command=delete_student)
    delete_btn.place(x=130, y=160, width=140)

    afficher_btn = tk.Button(admin_page_fm, text='Afficher Étudiants',
                             font=('Bold', 10), bg='white', fg=bg_color,
                             command=afficher_etudiants)
    afficher_btn.place(x=130, y=200, width=140)
    
    # Bouton pour revenir au menu
    home_btn = tk.Button(admin_page_fm, text='Menu', font=('bold', 15),
                     bg='white', fg=bg_color, bd=0, command=forward_to_welcome_page)
    home_btn.place(x=20, y=480, width=140)


    # Affichage du frame
    admin_page_fm.pack(pady=30)
    admin_page_fm.pack_propagate(False)
    admin_page_fm.configure(width=400, height=540, bg=bg_color)

student_gender = tk.StringVar()
class_list = ['DEV101','DEV102','DEV201','DEV202','1COM','1COMPT','2COM','2COMPT','AA101','AA102','GE101','GE102','GEOCM204','ID101','ID201']

def add_account_page():
    def forward_to_welcome_page():
        add_account_page_fm.destroy()
        root.update()
        welcome_page()

    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def enregistrer_donnees():
        id_etudiant = student_id.get()
        nom = student_name_ent.get().strip()
        genre = student_gender.get()
        age = student_age_ent.get().strip()
        contact = student_contact_ent.get().strip()
        groupe = select_class_btn.get().strip()
        email = student_email_ent.get().strip()
        motdepasse = account_password_ent.get().strip()

        if not all([id_etudiant, nom, genre, age, contact, groupe, email, motdepasse]):
            messagebox.showwarning("Champ vide", "Veuillez remplir tous les champs obligatoires.")
            return

        if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', nom):
            messagebox.showerror("Erreur", "Nom invalide. Utilisez uniquement des lettres et espaces.")
            return

        if not age.isdigit() or not (16 <= int(age) <= 40):
            messagebox.showerror("Erreur", "Âge doit être un nombre entre 16 et 40.")
            return


        if not re.match(r'^06\d{8}$', contact):
            messagebox.showerror("Erreur", "Le numéro doit commencer par 06 et contenir exactement 10 chiffres.")
            return


        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messagebox.showerror("Erreur", "Format email invalide.")
            return

        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', motdepasse):
            messagebox.showerror("Erreur", "Mot de passe: 8 caractères min, lettres et chiffres.")
            return

        motdepasse_hash = hash_password(motdepasse)

        file_exists = os.path.isfile("etudiants.csv")
        with open("etudiants.csv", mode="a", newline="", encoding="utf-8") as fichier:
            writer = csv.writer(fichier)
            if not file_exists:
                writer.writerow(["ID", "Nom", "Genre", "Age", "Contact", "Groupe", "Email", "Motdepasse"])
            writer.writerow([id_etudiant, nom, genre, age, contact, groupe, email, motdepasse_hash])
        
        messagebox.showinfo("Succès", "Inscription enregistrée avec succès!")
        forward_to_welcome_page()

    add_account_page_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)

    # ID généré une seule fois ici
    new_id = str(random.randint(1000, 9999))

    # Élément de saisie ID visible et défini ici
    student_id_lb = tk.Label(add_account_page_fm, text='Votre ID:', font=('bold', 12))
    student_id_lb.place(x=240, y=35)
    student_id = tk.Entry(add_account_page_fm, font=('bold', 18), bd=0)
    student_id.place(x=380, y=35, width=80)
    student_id.insert(tk.END, new_id)
    student_id.config(state='readonly')

    id_info_lb = tk.Label(add_account_page_fm, text="""ID généré automatiquement!\nN'oubliez pas c'est avec ce ID\nque vous allez vous connecter.""", justify=tk.LEFT)
    id_info_lb.place(x=240, y=65)

    # Les autres champs
    add_pic_section_fm = tk.Frame(add_account_page_fm, highlightbackground=bg_color, highlightthickness=2)
    add_pic_btn = tk.Button(add_pic_section_fm, image=add_student_pic_icon, bd=0)
    add_pic_btn.pack()
    add_pic_section_fm.place(x=5, y=5, width=105, height=105)

    student_name_lb = tk.Label(add_account_page_fm, text="Nom Complet :", font=('bold', 15))
    student_name_lb.place(x=5, y=130)
    student_name_ent = tk.Entry(add_account_page_fm, font=('bold', 15),
                                highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2)
    student_name_ent.place(x=5, y=160, width=180)

    student_gender_lb = tk.Label(add_account_page_fm, text='Selectionne ton Genre:', font=('bold', 12))
    student_gender_lb.place(x=5, y=210)

    male_gender_btn = tk.Radiobutton(add_account_page_fm, text='Homme', font=('bold', 12),
                                     variable=student_gender, value='Homme')
    male_gender_btn.place(x=5, y=235)

    female_gender_btn = tk.Radiobutton(add_account_page_fm, text='Femme', font=('bold', 12),
                                       variable=student_gender, value='Femme')
    female_gender_btn.place(x=75, y=235)

    student_gender.set('Homme')

    student_age_lb = tk.Label(add_account_page_fm, text='Entrez votre âge:', font=('bold', 12))
    student_age_lb.place(x=5, y=275)
    student_age_ent = tk.Entry(add_account_page_fm, font=('bold', 15),
                               highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2)
    student_age_ent.place(x=5, y=305, width=180)

    student_contact_lb = tk.Label(add_account_page_fm, text='Entrez votre Contact:', font=('bold', 12))
    student_contact_lb.place(x=5, y=360)
    student_contact_ent = tk.Entry(add_account_page_fm, font=('bold', 15),
                                   highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2)
    student_contact_ent.place(x=5, y=390, width=180)

    student_class_lb = tk.Label(add_account_page_fm, text='Entrez votre Groupe:', font=('bold', 12))
    student_class_lb.place(x=5, y=445)
    select_class_btn = Combobox(add_account_page_fm, font=('bold', 15), state='readonly', values=class_list)
    select_class_btn.place(x=5, y=475, width=180, height=30)

    student_email_lb = tk.Label(add_account_page_fm, text='Entrez votre E-Mail:', font=('bold', 12))
    student_email_lb.place(x=240, y=130)
    student_email_ent = tk.Entry(add_account_page_fm, font=('bold', 15),
                                 highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2)
    student_email_ent.place(x=240, y=160, width=180)

    email_info_lb = tk.Label(add_account_page_fm, text="""Via l'adresse E-Mail vous pouvez\nrécupérer le MOT DE PASSE!\nEn cas de perte.""", justify=tk.LEFT)
    email_info_lb.place(x=240, y=200)

    account_password_lb = tk.Label(add_account_page_fm, text='Créer un mot de passe:', font=('bold', 12))
    account_password_lb.place(x=240, y=275)
    account_password_ent = tk.Entry(add_account_page_fm, font=('bold', 15),
                                    highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2)
    account_password_ent.place(x=240, y=307, width=180)

    account_password_info_lb = tk.Label(add_account_page_fm, text="""Via le MDP créé et l'ID donné\nvous allez vous connecter.""", justify=tk.LEFT)
    account_password_info_lb.place(x=240, y=345)

    home_btn = tk.Button(add_account_page_fm, text='Menu', font=('bold', 15),
                         bg='red', fg='white', bd=0, command=forward_to_welcome_page)
    home_btn.place(x=240, y=420)

    submit_btn = tk.Button(add_account_page_fm, text='Valider', font=('bold', 15),
                           bg=bg_color, fg='white', bd=0, command=enregistrer_donnees)
    submit_btn.place(x=360, y=420)

    add_account_page_fm.pack(pady=5)
    add_account_page_fm.pack_propagate(False)
    add_account_page_fm.configure(width=480, height=580)

welcome_page()
root.mainloop()
