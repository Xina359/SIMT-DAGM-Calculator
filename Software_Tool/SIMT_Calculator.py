# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

class SIMT_Calculator:
    def __init__(self, root):
        self.root = root
        self.current_lang = 'en'  # 默认语言：英文 ('en' or 'cn')
        
        # --- 语言资源字典 ---
        self.texts = {
            'title': {'en': "SIMT Margin Calculator (Paper Companion)", 'cn': "SIMT 误差计算器 (论文配套工具)"},
            'tab1': {'en': "Planning (DAGM)", 'cn': "计划阶段 (DAGM)"},
            'tab2': {'en': "Daily IGRT (QA)", 'cn': "每日 IGRT (QA)"},
            'switch_btn': {'en': "Switch to Chinese", 'cn': "Switch to English"},
            
            # Tab 1 Content
            't1_instr': {
                'en': "Calculate Distance-Adaptive Geometric Margin (DAGM)\nFormula: M = Trans + Dist * sin(2.45 * σ)",
                'cn': "计算距离适应性几何边界 (DAGM)\n公式: M = 平移 + 距离 * sin(2.45 * σ)"
            },
            'lbl_dist': {'en': "Distance to Isocenter (mm):", 'cn': "靶区距离等中心 (mm):"},
            'lbl_sigma': {'en': "Rotational Error Sigma σ (deg):", 'cn': "旋转误差标准差 σ (度):"},
            'lbl_trans': {'en': "Translational Margin (mm):", 'cn': "平移边界基数 (mm):"},
            'btn_calc_dagm': {'en': "Calculate DAGM", 'cn': "计算 DAGM 推荐值"},
            'res_default': {'en': "Result will be shown here", 'cn': "结果将显示在这里"},
            'res_dagm': {
                'en': "Distance Effect: {:.2f} mm\n(Rayleigh P95, k=2.45)\n\nRecommended DAGM: {:.2f} mm",
                'cn': "距离效应分量: {:.2f} mm\n(瑞利分布 P95, k=2.45)\n\n推荐 DAGM 总边界: {:.2f} mm"
            },
            
            # Tab 2 Content
            't2_instr': {
                'en': "Calculate Max Geometric Error (TRE) for Daily QA\nCheck if residual error is within tolerance",
                'cn': "计算单次治疗最大几何偏差 (TRE)\n评估当日残留误差是否可接受"
            },
            'lbl_rot_meas': {'en': "Measured Residual Rotation (deg):", 'cn': "今日 IGRT 残留旋转读数 (度):"},
            'btn_calc_tre': {'en': "Calculate Current TRE", 'cn': "计算当前偏差 (TRE)"},
            'res_tre': {
                'en': "Max Geometric Error: {:.2f} mm\nStatus: {}",
                'cn': "最大几何偏差: {:.2f} mm\n状态: {}"
            },
            'safe': {'en': "Safe (< 1.0 mm)", 'cn': "安全 (< 1.0 mm)"},
            'warning': {'en': "Warning (> 1.0 mm)", 'cn': "警告 (> 1.0 mm)"},
            
            # Errors
            'err_title': {'en': "Input Error", 'cn': "输入错误"},
            'err_msg': {'en': "Please enter valid numbers.", 'cn': "请输入有效的数字。"}
        }

        self.setup_ui()
        self.update_texts() # 初始化文本

    def setup_ui(self):
        self.root.geometry("550x500")
        
        # 顶部切换语言按钮
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(fill='x', padx=10, pady=5)
        self.btn_lang = ttk.Button(self.top_frame, command=self.toggle_language)
        self.btn_lang.pack(side='right')

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True, fill='both')
        
        self.frame1 = ttk.Frame(self.notebook)
        self.frame2 = ttk.Frame(self.notebook)
        self.notebook.add(self.frame1)
        self.notebook.add(self.frame2)
        
        # --- Tab 1 UI Setup ---
        self.lbl_t1_instr = ttk.Label(self.frame1, justify="center", font=("Arial", 10, "italic"))
        self.lbl_t1_instr.pack(pady=10)
        
        self.lbl_d1 = ttk.Label(self.frame1)
        self.lbl_d1.pack()
        self.entry_d = ttk.Entry(self.frame1)
        self.entry_d.pack()
        self.entry_d.insert(0, "125")
        
        self.lbl_sigma = ttk.Label(self.frame1)
        self.lbl_sigma.pack()
        self.entry_sigma = ttk.Entry(self.frame1)
        self.entry_sigma.pack()
        self.entry_sigma.insert(0, "0.5")
        
        self.lbl_trans = ttk.Label(self.frame1)
        self.lbl_trans.pack()
        self.entry_trans = ttk.Entry(self.frame1)
        self.entry_trans.pack()
        self.entry_trans.insert(0, "0.7")
        
        self.btn_calc1 = ttk.Button(self.frame1, command=self.calculate_dagm)
        self.btn_calc1.pack(pady=20)
        
        self.res_lbl1 = ttk.Label(self.frame1, font=("Arial", 12, "bold"))
        self.res_lbl1.pack()

        # --- Tab 2 UI Setup ---
        self.lbl_t2_instr = ttk.Label(self.frame2, justify="center", font=("Arial", 10, "italic"))
        self.lbl_t2_instr.pack(pady=10)
        
        self.lbl_d2 = ttk.Label(self.frame2)
        self.lbl_d2.pack()
        self.entry_d2 = ttk.Entry(self.frame2)
        self.entry_d2.pack()
        self.entry_d2.insert(0, "150")
        
        self.lbl_rot = ttk.Label(self.frame2)
        self.lbl_rot.pack()
        self.entry_rot = ttk.Entry(self.frame2)
        self.entry_rot.pack()
        self.entry_rot.insert(0, "0.8")
        
        self.btn_calc2 = ttk.Button(self.frame2, command=self.calculate_tre)
        self.btn_calc2.pack(pady=20)
        
        self.res_lbl2 = ttk.Label(self.frame2, font=("Arial", 12, "bold"))
        self.res_lbl2.pack()

    def toggle_language(self):
        self.current_lang = 'cn' if self.current_lang == 'en' else 'en'
        self.update_texts()

    def update_texts(self):
        L = self.current_lang
        T = self.texts
        
        # Title & Tabs
        self.root.title(T['title'][L])
        self.notebook.tab(self.frame1, text=T['tab1'][L])
        self.notebook.tab(self.frame2, text=T['tab2'][L])
        self.btn_lang.config(text=T['switch_btn'][L])
        
        # Tab 1
        self.lbl_t1_instr.config(text=T['t1_instr'][L])
        self.lbl_d1.config(text=T['lbl_dist'][L])
        self.lbl_sigma.config(text=T['lbl_sigma'][L])
        self.lbl_trans.config(text=T['lbl_trans'][L])
        self.btn_calc1.config(text=T['btn_calc_dagm'][L])
        if "Rayleigh" not in self.res_lbl1.cget("text") and "瑞利" not in self.res_lbl1.cget("text"):
             self.res_lbl1.config(text=T['res_default'][L])
        
        # Tab 2
        self.lbl_t2_instr.config(text=T['t2_instr'][L])
        self.lbl_d2.config(text=T['lbl_dist'][L])
        self.lbl_rot.config(text=T['lbl_rot_meas'][L])
        self.btn_calc2.config(text=T['btn_calc_tre'][L])
        if "Max" not in self.res_lbl2.cget("text") and "最大" not in self.res_lbl2.cget("text"):
            self.res_lbl2.config(text=T['res_default'][L])

    def calculate_dagm(self):
        try:
            d = float(self.entry_d.get())
            sigma = float(self.entry_sigma.get())
            trans_m = float(self.entry_trans.get())
            
            # --- 核心算法 ---
            k = 2.45 # Rayleigh P95
            angle_rad = np.deg2rad(sigma * k) # 输入度 -> 转弧度
            rot_margin = d * np.sin(angle_rad)
            total_margin = trans_m + rot_margin
            
            L = self.current_lang
            res_str = self.texts['res_dagm'][L].format(rot_margin, total_margin)
            self.res_lbl1.config(text=res_str, foreground="blue")
            
        except ValueError:
            self.show_error()

    def calculate_tre(self):
        try:
            d = float(self.entry_d2.get())
            rot = float(self.entry_rot.get())
            
            # --- 核心算法 ---
            # 物理真值计算
            tre = d * np.sin(np.deg2rad(rot))
            
            L = self.current_lang
            status = self.texts['safe'][L] if tre < 1.0 else self.texts['warning'][L]
            color = "green" if tre < 1.0 else "red"
            
            res_str = self.texts['res_tre'][L].format(tre, status)
            self.res_lbl2.config(text=res_str, foreground=color)
            
        except ValueError:
            self.show_error()

    def show_error(self):
        L = self.current_lang
        messagebox.showerror(self.texts['err_title'][L], self.texts['err_msg'][L])

if __name__ == "__main__":
    root = tk.Tk()
    app = SIMT_Calculator(root)
    root.mainloop()
