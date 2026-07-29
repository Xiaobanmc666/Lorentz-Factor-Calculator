import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import sys
from decimal import Decimal, getcontext

getcontext().prec = 60
getcontext().rounding = "ROUND_HALF_EVEN"
C = Decimal("299792458")


def get_external_resource_path(relative_path):
    """
    源码：读取py脚本所在目录
    EXE：读取exe程序同级目录，languages、fonts放在exe外面
    """
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)


class LorentzFactorAppV2:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x720")
        self.root.minsize(800, 650)
        self.root.title("Lorentz Factor Calculator v2.0.0")

        self.lang_folder = get_external_resource_path("languages")
        self.fonts_folder = get_external_resource_path("fonts")

        if not os.path.isdir(self.lang_folder):
            messagebox.showerror(
                "Missing Folder",
                f"无法找到languages语言文件夹\n路径：{self.lang_folder}\n请将languages放置到exe同一目录！"
            )
        if not os.path.isdir(self.fonts_folder):
            messagebox.showwarning(
                "Missing Fonts Folder",
                f"fonts字体文件夹不存在 {self.fonts_folder}\n程序继续运行，使用系统自带字体"
            )

        self.load_custom_fonts()
        available_fonts = list(self.root.tk.call("font", "families"))

        def pick_font(prefer_list, size=11, bold=False):
            weight = "bold" if bold else "normal"
            for fname in prefer_list:
                if fname in available_fonts:
                    return (fname, size, weight)
            return ("", size, weight)

        self.FONT_UI = pick_font(["Noto Sans", "Microsoft YaHei", "SimHei", "Segoe UI", "Arial"], 11)
        self.FONT_UI_BOLD = pick_font(["Noto Sans", "Microsoft YaHei", "SimHei", "Segoe UI", "Arial"], 11, bold=True)
        self.FONT_MONO = pick_font(["Consolas", "Courier New", "Lucida Console"], 10)

        self.lang_data = {}
        self.language_list = [
            ("简体中文", "zh-CN.json"),
            ("繁體中文", "zh-TW.json"),
            ("English", "en.json"),
            ("日本語", "ja.json"),
            ("한국어", "ko.json"),
            ("Deutsch", "de.json"),
            ("Français", "fr.json"),
            ("Español", "es.json"),
            ("Русский", "ru.json"),
            ("Português", "pt.json"),
            ("Italiano", "it.json")
        ]
        self.current_lang_idx = 2
        self.load_language(self.language_list[self.current_lang_idx][1])

        self.setup_style()
        self.build_menubar()
        self.widget_ref = {}
        self.build_gui()

    def get_lang(self, key, fallback_text):
        return self.lang_data.get(key, fallback_text)

    def load_custom_fonts(self):
        if not os.path.isdir(self.fonts_folder):
            return
        for filename in os.listdir(self.fonts_folder):
            fn_low = filename.lower()
            if fn_low.endswith(".ttf") or fn_low.endswith(".otf"):
                full = os.path.join(self.fonts_folder, filename)
                try:
                    self.root.tk.call("font", "create", full)
                except Exception:
                    pass

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", font=self.FONT_UI)
        style.configure("TButton", padding=(12, 5))
        style.map(
            "TButton",
            background=[("active", "#4068a0"), ("!active", "#547cb8")],
            foreground=[("active", "white"), ("!active", "white")]
        )
        style.configure("TLabelframe", padding=14)
        style.configure("TLabelframe.Label", font=self.FONT_UI_BOLD)

    def load_language(self, filename):
        self.lang_data = {}
        path = os.path.join(self.lang_folder, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.lang_data = json.load(f)
        except Exception as e:
            messagebox.showwarning("Language Load Failed", f"加载 {filename} 失败\n{e}")
            self.lang_data = {}

    def build_menubar(self):
        self.menubar = tk.Menu(self.root, tearoff=0)
        self.root.config(menu=self.menubar)
        menu_settings = tk.Menu(self.menubar, tearoff=0)
        menu_lang = tk.Menu(menu_settings, tearoff=0)
        for idx, (display_name, json_file) in enumerate(self.language_list):
            def callback(i=idx):
                self.switch_language_by_index(i)
            menu_lang.add_command(label=display_name, command=callback)
        menu_settings.add_cascade(label=self.get_lang("menu_settings", "Settings"), menu=menu_lang)
        menu_settings.add_separator()
        menu_settings.add_command(label=self.get_lang("menu_about", "About"), command=self.show_about_dialog)
        self.menubar.add_cascade(label=self.get_lang("menu_settings", "Settings"), menu=menu_settings)

    def show_about_dialog(self):
        win = tk.Toplevel(self.root)
        win.geometry("620x440")
        win.minsize(520,360)
        win.resizable(False, False)
        win.title(self.get_lang("about_title", "About Lorentz Factor Calculator"))
        win.transient(self.root)
        win.update_idletasks()
        ww = win.winfo_width()
        wh = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - ww // 2
        y = (win.winfo_screenheight() // 2) - wh // 2
        win.geometry(f"{ww}x{wh}+{x}+{y}")
        win.grab_set()

        frame = ttk.Frame(win, padding=18)
        frame.pack(fill=tk.BOTH, expand=True)
        st = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=self.FONT_UI, bg="#f7f8fa")
        st.pack(fill=tk.BOTH, expand=True, pady=(0,14))
        st.insert(tk.END, self.get_lang("about_content", "Lorentz Factor Calculator\nCC0 Public Domain"))
        st.configure(state="disabled")
        ttk.Button(frame, text="OK", command=win.destroy).pack()

    def switch_language_by_index(self, idx):
        self.current_lang_idx = idx
        disp_name, fname = self.language_list[idx]
        self.load_language(fname)
        self.root.title(self.get_lang("window_title", "Lorentz Factor Calculator v2.0.0"))
        self.refresh_all_ui_text()
        self.txt_result.delete(1.0, tk.END)
        if self.var_speed.get().strip():
            self.do_calculate()

    def refresh_all_ui_text(self):
        self.widget_ref["lab_input_speed"]["text"] = self.get_lang("input_speed", "Speed (m/s):")
        self.widget_ref["lab_earth_note"]["text"] = self.get_lang("earth_one_sec_note", "Note: Earth‑frame time = 1s")
        self.widget_ref["lab_result_title"]["text"] = self.get_lang("result_header", "Calculation Result")
        self.btn_calc.config(text=self.get_lang("calc_button", "Calculate"))
        self.build_menubar()

    def build_gui(self):
        main_frame = ttk.Frame(self.root, padding=16)
        main_frame.pack(fill=tk.BOTH, expand=True)

        input_frame = ttk.LabelFrame(main_frame, padding=12)
        input_frame.pack(fill=tk.X, pady=(0,12))

        self.widget_ref["lab_input_speed"] = ttk.Label(input_frame, text=self.get_lang("input_speed", "Speed(m/s):"), font=self.FONT_UI)
        self.widget_ref["lab_input_speed"].grid(row=0, column=0, padx=8, pady=10, sticky="w")

        self.var_speed = tk.StringVar()
        self.entry_speed = ttk.Entry(input_frame, textvariable=self.var_speed, width=52, font=self.FONT_MONO)
        self.entry_speed.grid(row=0, column=1, padx=8, pady=10)

        self.btn_calc = ttk.Button(input_frame, text=self.get_lang("calc_button", "Calculate"), command=self.do_calculate)
        self.btn_calc.grid(row=0, column=2, padx=14, pady=10)

        self.widget_ref["lab_earth_note"] = ttk.Label(
            main_frame,
            text=self.get_lang("earth_one_sec_note", "Note: Earth‑frame time = 1s"),
            foreground="#2c4b82",
            font=self.FONT_UI
        )
        self.widget_ref["lab_earth_note"].pack(pady=(0,10), anchor="w")
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=6)

        res_frame = ttk.LabelFrame(main_frame, padding=10)
        res_frame.pack(fill=tk.BOTH, expand=True, pady=(8,0))
        self.widget_ref["lab_result_title"] = ttk.Label(
            res_frame,
            text=self.get_lang("result_header", "Calculation Result"),
            font=self.FONT_UI_BOLD
        )
        self.widget_ref["lab_result_title"].pack(anchor="nw", pady=(0,6))

        self.txt_result = scrolledtext.ScrolledText(
            res_frame,
            wrap=tk.WORD,
            font=self.FONT_MONO,
            bg="#f4f6f9",
            relief=tk.GROOVE,
            padx=8,
            pady=8
        )
        self.txt_result.pack(fill=tk.BOTH, expand=True)

    def do_calculate(self):
        content = ""
        try:
            v_text = self.var_speed.get().strip()
            v = Decimal(v_text)
            if v < 0:
                content += self.get_lang("err_negative", "速度不能为负数！")+"\n"
            elif v >= C:
                content += self.get_lang("err_speed_over_c", "速度不能达到或超过光速 299792458 m/s！")+"\n"
            else:
                beta = v / C
                gamma = Decimal(1) / ((Decimal(1) - beta * beta).sqrt())
                dt_earth = Decimal(1)
                dt_moving = dt_earth / gamma
                L0 = Decimal(1)
                L_obs = L0 / gamma
                gamma_minus_1 = gamma - Decimal(1)

                content += self.get_lang("physics_title", "狭义相对论计算结果") + "\n\n"
                content += f"{self.get_lang('lbl_v','速度 v')} : {v} m/s\n"
                content += f"{self.get_lang('lbl_beta','速度比 β=v/c')} : {beta}\n"
                content += f"{self.get_lang('lbl_gamma','洛伦兹因子 γ')} : {gamma}\n"
                content += f"{self.get_lang('lbl_gamma_diff','γ‑1（相对论微小差值）')} : {gamma_minus_1}\n\n"

                content += self.get_lang("dilate_header","■ 时间膨胀") + "\n"
                content += f"{self.get_lang('ref_earth_frame','地球惯性系流逝时间')} : {dt_earth} s\n"
                content += f"{self.get_lang('ref_moving_frame','运动物体固有时（物体自身经历的时间）')} : {dt_moving} s\n"
                content += self.get_lang("desc_time_dilate","物理说明：运动参考系时钟走得更慢。地球上过去1秒，高速物体只经历τ秒。这是时空本身固有效应，不是时钟机械故障。") + "\n\n"

                content += self.get_lang("length_contract_header","■ 长度收缩（固有长度 L₀ = 1 米）") + "\n"
                content += f"{self.get_lang('ref_rest_length','物体静止系下固有长度')} : {L0} m\n"
                content += f"{self.get_lang('ref_obs_length','地面静止观测者测得的长度')} : {L_obs} m\n"
                content += self.get_lang("desc_length_contract","物理说明：空间沿运动方向收缩。物体自身参考系长度不变；静止观测者测得更短。属于时空几何真实效应，不是物体发生物理形变。") + "\n"
        except ValueError:
            content += self.get_lang("err_invalid_input","输入无效，请输入合法十进制数字。")
        except Exception as e:
            content += f"Exception: {str(e)}"

        self.txt_result.delete(1.0, tk.END)
        self.txt_result.insert(tk.END, content)


if __name__ == "__main__":
    root = tk.Tk()
    app = LorentzFactorAppV2(root)
    root.mainloop()