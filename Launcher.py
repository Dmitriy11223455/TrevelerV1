import pygame 
import customtkinter as ctk

from  Treveler import start_game 

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class GameLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(" Launcher X")
        self.geometry("600x800")
        self.resizable(False, False)

        
        self.my_levels = ["Level1", "Level2", "Level3", "Level4"]
        
        self.translations = {
            "Русский": {
                "title": "ЛАУНЧЕР ИГРЫ", "language": "Язык:", "level": "Выберите уровень:", "theme": "Тема:", "play": "ИГРАТЬ"
            },
            "English": {
                "title": "GAME LAUNCHER", "language": "Language:", "level": "Select Level:", "theme": "Theme:", "play": "PLAY"
            }
            
        
        }
        self.current_lang = "Русский"
        

        
        self.title_label = ctk.CTkLabel(self, text=self.translations[self.current_lang]["title"], font=("Arial", 24, "bold"))
        self.title_label.pack(pady=30)

        
        self.lang_label = ctk.CTkLabel(self, text=self.translations[self.current_lang]["language"], font=("Arial", 14))
        self.lang_label.pack(pady=(15, 15))
        self.lang_menu = ctk.CTkOptionMenu(self, values=["Русский", "English"], command=self.change_language)
        self.lang_menu.set(self.current_lang)
        self.lang_menu.pack(pady=10)

        
        self.level_label = ctk.CTkLabel(self, text=self.translations[self.current_lang]["level"], font=("Arial", 14))
        self.level_label.pack(pady=(20, 5))
        self.level_menu = ctk.CTkOptionMenu(self, values=self.my_levels)
        self.level_menu.set(self.my_levels[0])
        self.level_menu.pack(pady=5)
        

        
        self.theme_label = ctk.CTkLabel(self, text=self.translations[self.current_lang]["theme"], font=("Arial", 14))
        self.theme_label.pack(pady=(20, 5))
        self.theme_menu = ctk.CTkOptionMenu(self, values=["System", "Dark", "Light"], command=ctk.set_appearance_mode)
        self.theme_menu.set("System")
        self.theme_menu.pack(pady=5)

        
        self.play_button = ctk.CTkButton(
            self, text=self.translations[self.current_lang]["play"], font=("Arial", 18, "bold"),
            fg_color="#228B22", hover_color="#006400", height=50, command=self.launch_game,
        )
        self.play_button.pack(pady=50, fill="x", padx=40)

    def change_language(self, choice):
        self.current_lang = choice
        t = self.translations[self.current_lang]
        self.title_label.configure(text=t["title"])
        self.lang_label.configure(text=t["language"])
        self.level_label.configure(text=t["level"])
        self.theme_label.configure(text=t["theme"])
        self.play_button.configure(text=t["play"])
        

    def launch_game(self):
        selected_level = self.level_menu.get()
        self.destroy() 
        
    
        start_game(selected_level) 

if __name__ == "__main__":
    app = GameLauncher()
    app.mainloop()
