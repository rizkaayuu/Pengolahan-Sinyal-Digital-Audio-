import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import Tk, Button
from PIL import Image, ImageTk
from tkinter import messagebox
import librosa
import noisereduce as nr
import numpy as np
import soundfile as sf
import shutil
import os

class CleanifyPro:
    def __init__(self, root):
        self.root = root
        self.root.title("CleanifyPro")

        self.frame_home = tk.Frame(root)
        self.frame_about = tk.Frame(root)
        self.frame_start = tk.Frame(root)
        self.frame_continue = tk.Frame(root)
        self.frame_upload_success = tk.Frame(root)

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        self.root.geometry(f"{screen_width}x{screen_height - 60}+0+0")

        try:
            self.background_image = Image.open("1.png")
            self.background_image = self.background_image.resize((screen_width, screen_height - 60), Image.Resampling.LANCZOS)
            self.background_image_tk = ImageTk.PhotoImage(self.background_image)
        except FileNotFoundError:
            self.background_image_tk = None
            print("File '1.png' tidak ditemukan.")

        self.uploaded_file_path = None
        self.button_continue = None  
        self.filtered_audio_path = None  

        self.show_home()

    def add_background(self, frame):
        if self.background_image_tk:
            label_background = tk.Label(frame, image=self.background_image_tk)
            label_background.image = self.background_image_tk  
            label_background.place(x=0, y=0, relwidth=1, relheight=1)

    def apply_fir_filter(self, audio, sr, cutoff=200):
        from scipy.signal import firwin, lfilter
        nyquist = sr / 2
        numtaps = 1  
        fir_coeff = firwin(numtaps, cutoff / nyquist, pass_zero=True)
        filtered_audio = lfilter(fir_coeff, [1.0], audio)
        return filtered_audio

    def enhance_audio_with_filter(self, audio, sr, noise_duration=1.0, cutoff=200):
        noise_clip = audio[:int(noise_duration * sr)]
        audio_denoised = nr.reduce_noise(y=audio, sr=sr, y_noise=noise_clip)

        audio_filtered = self.apply_fir_filter(audio_denoised, sr, cutoff=cutoff)

        rms = np.sqrt(np.mean(audio_filtered**2))
        target_rms = rms * 3
        gain_factor = target_rms / rms
        audio_enhanced = audio_filtered * gain_factor

        return audio_enhanced

    def filter_audio(self, input_path, output_path):
        try:
            audio, sr = librosa.load(input_path, sr=None)
            enhanced_audio = self.enhance_audio_with_filter(audio, sr)
            sf.write(output_path, enhanced_audio, sr)
            return output_path
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            return None

    def show_home(self):
        for widget in self.frame_about.winfo_children() + self.frame_start.winfo_children() + self.frame_continue.winfo_children() + self.frame_upload_success.winfo_children():
            widget.destroy()

        img = Image.open("1.png")
        img = img.resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        label = tk.Label(self.frame_home, image=img_tk)
        label.image = img_tk
        label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.add_background(self.frame_home)

        img_home = Image.open("home_hitam.png").resize((145, 50), Image.Resampling.LANCZOS)
        self.image_home = ImageTk.PhotoImage(img_home) 
        self.home_button = tk.Button(self.frame_home, image=self.image_home, command=self.show_home, borderwidth=0)
        self.home_button.place(x=1023, y=19)
        
        img_about = Image.open("about_putih.PNG").resize((145, 50), Image.Resampling.LANCZOS)
        self.image_about = ImageTk.PhotoImage(img_about)  
        self.about_button = tk.Button(self.frame_home, image=self.image_about, command=self.show_about, borderwidth=0)
        self.about_button.place(x=1180, y=19)

        img_start = Image.open("filtering.PNG").resize((670, 103), Image.Resampling.LANCZOS)
        self.image_start = ImageTk.PhotoImage(img_start)  
        self.start_button = tk.Button(self.frame_home, image=self.image_start, command=self.show_start_page, borderwidth=0)
        self.start_button.place(x=325, y=365) 

        self.frame_home.pack(fill="both", expand=True)
        self.frame_about.pack_forget()
        self.frame_start.pack_forget()
        self.frame_continue.pack_forget()
        self.frame_upload_success.pack_forget()

    def show_about(self):
        for widget in self.frame_home.winfo_children() + self.frame_start.winfo_children() + self.frame_continue.winfo_children() + self.frame_upload_success.winfo_children():
            widget.destroy()

        img = Image.open("2.png")
        img = img.resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        label = tk.Label(self.frame_about, image=img_tk)
        label.image = img_tk
        label.place(x=0, y=0, relwidth=1, relheight=1)
        
        img_about = Image.open("about_hitam.PNG").resize((145, 50), Image.Resampling.LANCZOS)
        self.image_about = ImageTk.PhotoImage(img_about)  
        self.about_button = tk.Button(self.frame_about, image=self.image_about, command=self.show_about, borderwidth=0)
        self.about_button.place(x=1180, y=19)
        
        img_home = Image.open("home_putih.PNG").resize((145, 50), Image.Resampling.LANCZOS)
        self.image_home = ImageTk.PhotoImage(img_home)
        self.home_button = tk.Button(self.frame_about, image=self.image_home, command=self.show_home, borderwidth=0)
        self.home_button.place(x=1023, y=19)

        img_home2 = Image.open("continue_filtering.PNG").resize((290, 60), Image.Resampling.LANCZOS)
        self.image_home2 = ImageTk.PhotoImage(img_home2)
        self.home_button2 = Button(self.frame_about, image=self.image_home2, command=self.show_home, borderwidth=0)  # Panggil fungsi secara langsung
        self.home_button2.place(x=190, y=440)
        
        self.frame_about.pack(fill="both", expand=True)
        self.frame_home.pack_forget()
        self.frame_start.pack_forget()
        self.frame_continue.pack_forget()
        self.frame_upload_success.pack_forget()
        
    def show_home2(self):
        self.show_home()

    def show_start_page(self):
        for widget in self.frame_home.winfo_children() + self.frame_about.winfo_children() + self.frame_continue.winfo_children() + self.frame_upload_success.winfo_children():
            widget.destroy()

        img = Image.open("3.png")
        img = img.resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        label = tk.Label(self.frame_start, image=img_tk)
        label.image = img_tk
        label.place(x=0, y=0, relwidth=1, relheight=1)

        img_home = Image.open("home_hitam.png").resize((145, 50), Image.Resampling.LANCZOS)
        self.image_home = ImageTk.PhotoImage(img_home) 
        self.home_button = tk.Button(self.frame_start, image=self.image_home, command=self.show_home, borderwidth=0)
        self.home_button.place(x=1023, y=19)
        
        img_about = Image.open("about_putih.PNG").resize((145, 50), Image.Resampling.LANCZOS)
        self.image_about = ImageTk.PhotoImage(img_about)  
        self.about_button = tk.Button(self.frame_start, image=self.image_about, command=self.show_about, borderwidth=0)
        self.about_button.place(x=1180, y=19)
        
        img_upload = Image.open("upload.PNG").resize((190, 40), Image.Resampling.LANCZOS)
        self.image_upload = ImageTk.PhotoImage(img_upload)  
        self.upload_button = tk.Button(self.frame_start, image=self.image_upload, command=self.upload_file, borderwidth=0)
        self.upload_button.place(x=525, y=475)
        
        self.uploaded_file_label = tk.Label(self.frame_start, text='', bg="white", fg="black")
        self.uploaded_file_label.place(x=1023, y=22)

        self.frame_start.pack(fill="both", expand=True)
        self.frame_home.pack_forget()
        self.frame_about.pack_forget()
        self.frame_continue.pack_forget()
        self.frame_upload_success.pack_forget()

    def upload_file(self):
        self.uploaded_file_path = filedialog.askopenfilename(
            title="Pilih File untuk Diunggah",
            filetypes=[("Audio Files", "*.wav"), ("All Files", "*.*")]
        )
        if self.uploaded_file_path:
            self.uploaded_file_label.config(text=f"")
            messagebox.showinfo("Sukses", f"File {self.uploaded_file_path.split('/')[-1]} berhasil diunggah!")

            if not self.button_continue:
                self.button_continue = tk.Button(self.frame_start, text="Continue", command=self.show_continue_page)
                self.button_continue.place(x=280, y=20)

            self.show_upload_success()

    def show_upload_success(self):
        for widget in self.frame_home.winfo_children() + self.frame_about.winfo_children() + self.frame_start.winfo_children() + self.frame_continue.winfo_children():
            widget.destroy()

        img = Image.open("4.png")
        img = img.resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        label = tk.Label(self.frame_upload_success, image=img_tk)
        label.image = img_tk
        label.place(x=0, y=0, relwidth=1, relheight=1)

        img_home = Image.open("home_hitam.png").resize((145, 50), Image.Resampling.LANCZOS)
        self.image_home = ImageTk.PhotoImage(img_home) 
        self.home_button = tk.Button(self.frame_upload_success, image=self.image_home, command=self.show_home, borderwidth=0)
        self.home_button.place(x=1023, y=19)
        
        img_about = Image.open("about_putih.PNG").resize((145, 50), Image.Resampling.LANCZOS)
        self.image_about = ImageTk.PhotoImage(img_about)  
        self.about_button = tk.Button(self.frame_upload_success, image=self.image_about, command=self.show_about, borderwidth=0)
        self.about_button.place(x=1180, y=19)

        img_continue = Image.open("continue_filtering.PNG").resize((210, 65), Image.Resampling.LANCZOS)
        self.image_continue = ImageTk.PhotoImage(img_continue)  
        self.continue_button = tk.Button(self.frame_upload_success, image=self.image_continue, command=self.show_continue_page, borderwidth=0)
        self.continue_button.place(x=510, y=560)
        
        file_name = self.uploaded_file_path.split('/')[-1]
        formatted_text = "\n".join([file_name[i:i+20] for i in range(0, len(file_name), 20)])
        file_info_label = tk.Label(
            self.frame_upload_success,
            text=formatted_text,
            font=("Helvetica", 22),
            bg="white",
            fg="black",
            wraplength=200,  
            justify="center" 
        )
        file_info_label.place(x=550, y=480)

        
        self.frame_upload_success.pack(fill="both", expand=True)
        self.frame_home.pack_forget()
        self.frame_about.pack_forget()
        self.frame_start.pack_forget()
        self.frame_continue.pack_forget()

    def show_continue_page(self):
        for widget in self.frame_home.winfo_children() + self.frame_about.winfo_children() + self.frame_start.winfo_children() + self.frame_upload_success.winfo_children():
            widget.destroy()

        img = Image.open("5.png")
        img = img.resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        label = tk.Label(self.frame_continue, image=img_tk)
        label.image = img_tk
        label.place(x=0, y=0, relwidth=1, relheight=1)
        
        img_home = Image.open("home_hitam.png").resize((145, 50), Image.Resampling.LANCZOS)
        self.image_home = ImageTk.PhotoImage(img_home) 
        self.home_button = tk.Button(self.frame_continue, image=self.image_home, command=self.show_home, borderwidth=0)
        self.home_button.place(x=1023, y=19)
        
        img_about = Image.open("about_putih.PNG").resize((145, 50), Image.Resampling.LANCZOS)
        self.image_about = ImageTk.PhotoImage(img_about)  
        self.about_button = tk.Button(self.frame_continue, image=self.image_about, command=self.show_about, borderwidth=0)
        self.about_button.place(x=1180, y=19)

        img_start = Image.open("download.PNG").resize((670, 103), Image.Resampling.LANCZOS)
        self.image_start = ImageTk.PhotoImage(img_start)  
        self.start_button = tk.Button(self.frame_continue, image=self.image_start, command=self.download_audio, borderwidth=0)
        self.start_button.place(x=340, y=360) 

        self.frame_continue.pack(fill="both", expand=True)
        self.frame_home.pack_forget()
        self.frame_about.pack_forget()
        self.frame_start.pack_forget()
        self.frame_upload_success.pack_forget()

        self.process_audio()

    def process_audio(self):
        if self.uploaded_file_path:
            self.filtered_audio_path = "sada_filtered_output.wav"
            result_path = self.filter_audio(self.uploaded_file_path, self.filtered_audio_path)
            if result_path:
                self.filtered_audio_path = result_path
                messagebox.showinfo("Sukses", f"File {self.uploaded_file_path.split('/')[-1]} berhasil difilter!") 
            else:
                self.result_label.config(text="Terjadi kesalahan saat memfilter audio!")
                messagebox.showwarning("Peringatan", "Terjadi kesalahan saat memfilter audio!")
        else:
            self.result_label.config(text="Tidak ada file audio yang diunggah!")
            messagebox.showwarning("Peringatan", "Tidak ada file audio yang diunggah!")

    def download_audio(self):
        if self.filtered_audio_path and os.path.exists(self.filtered_audio_path):
            download_path = filedialog.asksaveasfilename(
                defaultextension=".wav", filetypes=[("Audio Files", "*.wav")],
                title="Simpan Audio"
            )
            if download_path:
                shutil.copy(self.filtered_audio_path, download_path)
                messagebox.showinfo("Sukses", "Audio hasil filter berhasil diunduh!")
        else:
            messagebox.showwarning("Peringatan", "Tidak ada audio yang siap diunduh atau file tidak ditemukan!")

root = tk.Tk()
app = CleanifyPro(root)

root.mainloop()
