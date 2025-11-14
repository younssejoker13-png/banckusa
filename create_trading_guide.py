#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont
import io

class TradingGuidePDF:
    def __init__(self, filename):
        self.filename = filename
        self.c = canvas.Canvas(filename, pagesize=A4)
        self.width, self.height = A4
        self.y_position = self.height - 2*cm
        
    def arabic_text(self, text):
        """تحويل النص العربي للعرض الصحيح"""
        reshaped_text = reshape(text)
        return get_display(reshaped_text)
    
    def draw_title(self, title, font_size=24):
        """رسم العنوان الرئيسي"""
        self.c.setFont("Helvetica-Bold", font_size)
        self.c.setFillColor(colors.HexColor("#1a1a1a"))
        text = self.arabic_text(title)
        text_width = self.c.stringWidth(text, "Helvetica-Bold", font_size)
        x = (self.width - text_width) / 2
        self.c.drawString(x, self.y_position, text)
        self.y_position -= 1.5*cm
        
    def draw_subtitle(self, subtitle, font_size=16):
        """رسم العنوان الفرعي"""
        self.c.setFont("Helvetica", font_size)
        self.c.setFillColor(colors.HexColor("#444444"))
        text = self.arabic_text(subtitle)
        text_width = self.c.stringWidth(text, "Helvetica", font_size)
        x = (self.width - text_width) / 2
        self.c.drawString(x, self.y_position, text)
        self.y_position -= 1*cm
        
    def draw_section_header(self, header, font_size=14):
        """رسم رأس القسم"""
        if self.y_position < 4*cm:
            self.c.showPage()
            self.y_position = self.height - 2*cm
            
        self.c.setFont("Helvetica-Bold", font_size)
        self.c.setFillColor(colors.HexColor("#2c5aa0"))
        text = self.arabic_text(header)
        text_width = self.c.stringWidth(text, "Helvetica-Bold", font_size)
        x = (self.width - text_width) / 2
        self.c.drawString(x, self.y_position, text)
        self.y_position -= 0.8*cm
        
    def draw_text(self, text, font_size=11, align='right', indent=0):
        """رسم نص عادي"""
        if self.y_position < 3*cm:
            self.c.showPage()
            self.y_position = self.height - 2*cm
            
        self.c.setFont("Helvetica", font_size)
        self.c.setFillColor(colors.HexColor("#333333"))
        text = self.arabic_text(text)
        
        if align == 'right':
            x = self.width - 3*cm - indent
            self.c.drawRightString(x, self.y_position, text)
        elif align == 'center':
            text_width = self.c.stringWidth(text, "Helvetica", font_size)
            x = (self.width - text_width) / 2
            self.c.drawString(x, self.y_position, text)
        else:
            x = 3*cm + indent
            self.c.drawString(x, self.y_position, text)
            
        self.y_position -= 0.6*cm
        
    def create_candle_image(self, candle_type, color, width=200, height=150):
        """إنشاء صورة شمعة يابانية"""
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        
        center_x = width // 2
        
        if candle_type == "bullish_engulfing":
            # شمعة هابطة صغيرة
            draw.rectangle([center_x-15, 50, center_x-5, 80], fill='red', outline='black', width=2)
            draw.line([center_x-10, 40, center_x-10, 50], fill='black', width=2)
            draw.line([center_x-10, 80, center_x-10, 90], fill='black', width=2)
            
            # شمعة صاعدة كبيرة
            draw.rectangle([center_x+5, 35, center_x+25, 95], fill=color, outline='black', width=2)
            draw.line([center_x+15, 25, center_x+15, 35], fill='black', width=2)
            draw.line([center_x+15, 95, center_x+15, 105], fill='black', width=2)
            
        elif candle_type == "bearish_engulfing":
            # شمعة صاعدة صغيرة
            draw.rectangle([center_x-15, 50, center_x-5, 80], fill='blue', outline='black', width=2)
            draw.line([center_x-10, 40, center_x-10, 50], fill='black', width=2)
            draw.line([center_x-10, 80, center_x-10, 90], fill='black', width=2)
            
            # شمعة هابطة كبيرة
            draw.rectangle([center_x+5, 35, center_x+25, 95], fill=color, outline='black', width=2)
            draw.line([center_x+15, 25, center_x+15, 35], fill='black', width=2)
            draw.line([center_x+15, 95, center_x+15, 105], fill='black', width=2)
            
        elif candle_type == "hammer":
            # شمعة المطرقة
            draw.rectangle([center_x-10, 40, center_x+10, 55], fill=color, outline='black', width=2)
            draw.line([center_x, 55, center_x, 110], fill='black', width=3)
            draw.line([center_x, 30, center_x, 40], fill='black', width=2)
            
        elif candle_type == "shooting_star":
            # شمعة الشهاب
            draw.line([center_x, 20, center_x, 70], fill='black', width=3)
            draw.rectangle([center_x-10, 70, center_x+10, 85], fill=color, outline='black', width=2)
            draw.line([center_x, 85, center_x, 95], fill='black', width=2)
            
        elif candle_type == "doji":
            # شمعة الدوجي
            draw.line([center_x, 25, center_x, 105], fill='black', width=2)
            draw.rectangle([center_x-8, 62, center_x+8, 68], fill='gray', outline='black', width=2)
            
        elif candle_type == "morning_star":
            # نجمة الصباح (3 شموع)
            # شمعة هابطة
            draw.rectangle([center_x-50, 35, center_x-35, 85], fill='red', outline='black', width=2)
            draw.line([center_x-42.5, 25, center_x-42.5, 35], fill='black', width=2)
            draw.line([center_x-42.5, 85, center_x-42.5, 95], fill='black', width=2)
            
            # شمعة صغيرة (دوجي)
            draw.line([center_x, 40, center_x, 90], fill='black', width=2)
            draw.rectangle([center_x-5, 63, center_x+5, 67], fill='gray', outline='black', width=2)
            
            # شمعة صاعدة
            draw.rectangle([center_x+35, 35, center_x+50, 85], fill=color, outline='black', width=2)
            draw.line([center_x+42.5, 25, center_x+42.5, 35], fill='black', width=2)
            draw.line([center_x+42.5, 85, center_x+42.5, 95], fill='black', width=2)
            
        elif candle_type == "evening_star":
            # نجمة المساء (3 شموع)
            # شمعة صاعدة
            draw.rectangle([center_x-50, 35, center_x-35, 85], fill='blue', outline='black', width=2)
            draw.line([center_x-42.5, 25, center_x-42.5, 35], fill='black', width=2)
            draw.line([center_x-42.5, 85, center_x-42.5, 95], fill='black', width=2)
            
            # شمعة صغيرة (دوجي)
            draw.line([center_x, 40, center_x, 90], fill='black', width=2)
            draw.rectangle([center_x-5, 63, center_x+5, 67], fill='gray', outline='black', width=2)
            
            # شمعة هابطة
            draw.rectangle([center_x+35, 35, center_x+50, 85], fill=color, outline='black', width=2)
            draw.line([center_x+42.5, 25, center_x+42.5, 35], fill='black', width=2)
            draw.line([center_x+42.5, 85, center_x+42.5, 95], fill='black', width=2)
            
        elif candle_type == "three_white_soldiers":
            # ثلاثة جنود بيض
            for i in range(3):
                x_offset = (i - 1) * 30
                y_start = 70 - (i * 15)
                y_end = 40 - (i * 15)
                draw.rectangle([center_x+x_offset-8, y_end, center_x+x_offset+8, y_start], 
                             fill=color, outline='black', width=2)
                draw.line([center_x+x_offset, y_end-10, center_x+x_offset, y_end], fill='black', width=2)
                draw.line([center_x+x_offset, y_start, center_x+x_offset, y_start+10], fill='black', width=2)
                
        elif candle_type == "three_black_crows":
            # ثلاثة غربان سوداء
            for i in range(3):
                x_offset = (i - 1) * 30
                y_start = 40 + (i * 15)
                y_end = 70 + (i * 15)
                draw.rectangle([center_x+x_offset-8, y_start, center_x+x_offset+8, y_end], 
                             fill=color, outline='black', width=2)
                draw.line([center_x+x_offset, y_start-10, center_x+x_offset, y_start], fill='black', width=2)
                draw.line([center_x+x_offset, y_end, center_x+x_offset, y_end+10], fill='black', width=2)
                
        elif candle_type == "piercing_line":
            # خط الاختراق
            # شمعة هابطة
            draw.rectangle([center_x-15, 35, center_x-5, 85], fill='red', outline='black', width=2)
            draw.line([center_x-10, 25, center_x-10, 35], fill='black', width=2)
            draw.line([center_x-10, 85, center_x-10, 95], fill='black', width=2)
            
            # شمعة صاعدة تخترق
            draw.rectangle([center_x+5, 45, center_x+15, 95], fill=color, outline='black', width=2)
            draw.line([center_x+10, 35, center_x+10, 45], fill='black', width=2)
            draw.line([center_x+10, 95, center_x+10, 105], fill='black', width=2)
            
        elif candle_type == "dark_cloud":
            # الغيمة السوداء
            # شمعة صاعدة
            draw.rectangle([center_x-15, 35, center_x-5, 85], fill='blue', outline='black', width=2)
            draw.line([center_x-10, 25, center_x-10, 35], fill='black', width=2)
            draw.line([center_x-10, 85, center_x-10, 95], fill='black', width=2)
            
            # شمعة هابطة تغطي
            draw.rectangle([center_x+5, 45, center_x+15, 95], fill=color, outline='black', width=2)
            draw.line([center_x+10, 35, center_x+10, 45], fill='black', width=2)
            draw.line([center_x+10, 95, center_x+10, 105], fill='black', width=2)
            
        elif candle_type == "tweezer_top":
            # قمة الملقط
            draw.rectangle([center_x-15, 35, center_x-5, 75], fill='blue', outline='black', width=2)
            draw.line([center_x-10, 25, center_x-10, 35], fill='black', width=2)
            draw.line([center_x-10, 75, center_x-10, 85], fill='black', width=2)
            
            draw.rectangle([center_x+5, 35, center_x+15, 75], fill=color, outline='black', width=2)
            draw.line([center_x+10, 25, center_x+10, 35], fill='black', width=2)
            draw.line([center_x+10, 75, center_x+10, 85], fill='black', width=2)
            
        elif candle_type == "tweezer_bottom":
            # قاع الملقط
            draw.rectangle([center_x-15, 45, center_x-5, 85], fill='red', outline='black', width=2)
            draw.line([center_x-10, 35, center_x-10, 45], fill='black', width=2)
            draw.line([center_x-10, 85, center_x-10, 95], fill='black', width=2)
            
            draw.rectangle([center_x+5, 45, center_x+15, 85], fill=color, outline='black', width=2)
            draw.line([center_x+10, 35, center_x+10, 45], fill='black', width=2)
            draw.line([center_x+10, 85, center_x+10, 95], fill='black', width=2)
        
        # حفظ الصورة في buffer
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        return ImageReader(img_buffer)
    
    def draw_candle_pattern(self, name, candle_type, color, description, entry, tp, sl):
        """رسم نمط شمعة مع الشرح"""
        if self.y_position < 10*cm:
            self.c.showPage()
            self.y_position = self.height - 2*cm
        
        # رسم إطار للنمط
        box_height = 9*cm
        box_y = self.y_position - box_height
        self.c.setStrokeColor(colors.HexColor("#e0e0e0"))
        self.c.setLineWidth(1)
        self.c.rect(2*cm, box_y, self.width - 4*cm, box_height)
        
        # اسم النمط
        self.c.setFont("Helvetica-Bold", 13)
        self.c.setFillColor(colors.HexColor("#1a1a1a"))
        text = self.arabic_text(name)
        text_width = self.c.stringWidth(text, "Helvetica-Bold", 13)
        x = (self.width - text_width) / 2
        self.c.drawString(x, self.y_position - 0.7*cm, text)
        
        # رسم الشمعة
        candle_img = self.create_candle_image(candle_type, color)
        img_width = 5*cm
        img_height = 3.5*cm
        img_x = (self.width - img_width) / 2
        img_y = self.y_position - 5*cm
        self.c.drawImage(candle_img, img_x, img_y, width=img_width, height=img_height)
        
        # الوصف
        desc_y = img_y - 0.8*cm
        self.c.setFont("Helvetica", 10)
        self.c.setFillColor(colors.HexColor("#333333"))
        
        # تقسيم الوصف لعدة أسطر
        lines = description.split('.')
        for line in lines:
            if line.strip():
                text = self.arabic_text(line.strip() + '.')
                text_width = self.c.stringWidth(text, "Helvetica", 10)
                x = (self.width - text_width) / 2
                self.c.drawString(x, desc_y, text)
                desc_y -= 0.5*cm
        
        # معلومات الدخول
        info_y = desc_y - 0.5*cm
        self.c.setFont("Helvetica-Bold", 10)
        
        # نقطة الدخول
        entry_text = self.arabic_text(f"نقطة الدخول: {entry}")
        self.c.setFillColor(colors.HexColor("#2c5aa0"))
        self.c.drawRightString(self.width - 3*cm, info_y, entry_text)
        
        # TP
        tp_text = self.arabic_text(f"TP: {tp}")
        self.c.setFillColor(colors.HexColor("#10b981"))
        self.c.drawRightString(self.width - 3*cm, info_y - 0.5*cm, tp_text)
        
        # SL
        sl_text = self.arabic_text(f"SL: {sl}")
        self.c.setFillColor(colors.HexColor("#ef4444"))
        self.c.drawRightString(self.width - 3*cm, info_y - 1*cm, sl_text)
        
        self.y_position -= (box_height + 0.5*cm)
    
    def create_guide(self):
        """إنشاء الدليل الكامل"""
        
        # صفحة الغلاف
        self.c.setFillColor(colors.HexColor("#1a1a1a"))
        self.c.rect(0, 0, self.width, self.height, fill=True)
        
        self.c.setFillColor(colors.white)
        self.c.setFont("Helvetica-Bold", 32)
        title = self.arabic_text("دليل الشموع اليابانية")
        text_width = self.c.stringWidth(title, "Helvetica-Bold", 32)
        self.c.drawString((self.width - text_width) / 2, self.height - 8*cm, title)
        
        self.c.setFont("Helvetica-Bold", 24)
        subtitle = self.arabic_text("للمحترفين في تداول الذهب")
        text_width = self.c.stringWidth(subtitle, "Helvetica-Bold", 24)
        self.c.drawString((self.width - text_width) / 2, self.height - 10*cm, subtitle)
        
        self.c.setFont("Helvetica", 14)
        desc = self.arabic_text("دليل شامل لأنماط الشموع اليابانية مع نقاط الدخول والخروج")
        text_width = self.c.stringWidth(desc, "Helvetica", 14)
        self.c.drawString((self.width - text_width) / 2, self.height - 12*cm, desc)
        
        # إضافة رمز الذهب
        self.c.setFont("Helvetica-Bold", 48)
        self.c.setFillColor(colors.HexColor("#FFD700"))
        self.c.drawString((self.width - 1.5*cm) / 2, self.height - 15*cm, "🏆")
        
        self.c.showPage()
        
        # صفحة المقدمة
        self.y_position = self.height - 2*cm
        self.draw_title("مقدمة", 20)
        
        intro_text = [
            "الشموع اليابانية هي أداة قوية لتحليل حركة الأسعار في الأسواق المالية.",
            "تم تطويرها في اليابان في القرن الثامن عشر لتداول الأرز.",
            "كل شمعة تمثل فترة زمنية محددة وتحتوي على أربعة عناصر أساسية:",
            "• سعر الافتتاح (Open)",
            "• سعر الإغلاق (Close)",
            "• أعلى سعر (High)",
            "• أدنى سعر (Low)",
            "",
            "الشموع الزرقاء 🔵 تشير إلى الشراء (السعر أغلق أعلى من الافتتاح)",
            "الشموع الحمراء 🔴 تشير إلى البيع (السعر أغلق أقل من الافتتاح)",
        ]
        
        for text in intro_text:
            self.draw_text(text, align='center')
        
        self.c.showPage()
        
        # أنماط الشموع الصاعدة (إشارات شراء)
        self.y_position = self.height - 2*cm
        self.draw_title("أنماط الشموع الصاعدة 🔵", 18)
        self.draw_subtitle("إشارات الشراء", 14)
        self.y_position -= 0.5*cm
        
        # 1. الابتلاع الصاعد
        self.draw_candle_pattern(
            "الابتلاع الصاعد (Bullish Engulfing)",
            "bullish_engulfing",
            "#3b82f6",
            "شمعة صاعدة كبيرة تبتلع الشمعة الهابطة السابقة بالكامل. إشارة قوية على انعكاس الاتجاه من هابط إلى صاعد",
            "عند إغلاق الشمعة الصاعدة الكبيرة",
            "مستوى المقاومة التالي أو 1:2 من نقطة الدخول",
            "أسفل قاع الشمعة الصاعدة"
        )
        
        # 2. المطرقة
        self.draw_candle_pattern(
            "المطرقة (Hammer)",
            "hammer",
            "#3b82f6",
            "شمعة بجسم صغير وظل سفلي طويل. تظهر في نهاية الاتجاه الهابط وتشير إلى انعكاس صاعد محتمل",
            "عند كسر أعلى الشمعة",
            "مستوى المقاومة أو 1.5:1 من نقطة الدخول",
            "أسفل الظل السفلي للمطرقة"
        )
        
        # 3. نجمة الصباح
        self.draw_candle_pattern(
            "نجمة الصباح (Morning Star)",
            "morning_star",
            "#3b82f6",
            "نمط من ثلاث شموع: شمعة هابطة كبيرة، شمعة صغيرة (دوجي)، ثم شمعة صاعدة كبيرة. إشارة انعكاس قوية جداً",
            "عند إغلاق الشمعة الصاعدة الثالثة",
            "مستوى المقاومة القوي أو 2:1 من نقطة الدخول",
            "أسفل قاع النمط الكامل"
        )
        
        self.c.showPage()
        self.y_position = self.height - 2*cm
        
        # 4. ثلاثة جنود بيض
        self.draw_candle_pattern(
            "ثلاثة جنود بيض (Three White Soldiers)",
            "three_white_soldiers",
            "#3b82f6",
            "ثلاث شموع صاعدة متتالية بأجسام كبيرة وظلال قصيرة. كل شمعة تفتح داخل جسم الشمعة السابقة وتغلق أعلى منها",
            "بعد إغلاق الشمعة الثالثة",
            "المقاومة التالية أو 2:1 من نقطة الدخول",
            "أسفل قاع الشمعة الأولى"
        )
        
        # 5. خط الاختراق
        self.draw_candle_pattern(
            "خط الاختراق (Piercing Line)",
            "piercing_line",
            "#3b82f6",
            "شمعة صاعدة تفتح أسفل إغلاق الشمعة الهابطة السابقة وتغلق فوق منتصفها. إشارة انعكاس صاعد",
            "عند إغلاق الشمعة الصاعدة",
            "مستوى المقاومة أو 1.5:1 من نقطة الدخول",
            "أسفل قاع الشمعة الصاعدة"
        )
        
        # 6. قاع الملقط
        self.draw_candle_pattern(
            "قاع الملقط (Tweezer Bottom)",
            "tweezer_bottom",
            "#3b82f6",
            "شمعتان متتاليتان بنفس القاع تقريباً. الأولى هابطة والثانية صاعدة. تشير إلى دعم قوي ومحتمل انعكاس صاعد",
            "عند كسر أعلى الشمعة الثانية",
            "المقاومة التالية أو 1.5:1 من نقطة الدخول",
            "أسفل القاع المشترك"
        )
        
        self.c.showPage()
        
        # أنماط الشموع الهابطة (إشارات بيع)
        self.y_position = self.height - 2*cm
        self.draw_title("أنماط الشموع الهابطة 🔴", 18)
        self.draw_subtitle("إشارات البيع", 14)
        self.y_position -= 0.5*cm
        
        # 1. الابتلاع الهابط
        self.draw_candle_pattern(
            "الابتلاع الهابط (Bearish Engulfing)",
            "bearish_engulfing",
            "#ef4444",
            "شمعة هابطة كبيرة تبتلع الشمعة الصاعدة السابقة بالكامل. إشارة قوية على انعكاس الاتجاه من صاعد إلى هابط",
            "عند إغلاق الشمعة الهابطة الكبيرة",
            "مستوى الدعم التالي أو 1:2 من نقطة الدخول",
            "أعلى قمة الشمعة الهابطة"
        )
        
        # 2. الشهاب
        self.draw_candle_pattern(
            "الشهاب (Shooting Star)",
            "shooting_star",
            "#ef4444",
            "شمعة بجسم صغير وظل علوي طويل. تظهر في نهاية الاتجاه الصاعد وتشير إلى انعكاس هابط محتمل",
            "عند كسر أسفل الشمعة",
            "مستوى الدعم أو 1.5:1 من نقطة الدخول",
            "أعلى الظل العلوي للشهاب"
        )
        
        # 3. نجمة المساء
        self.draw_candle_pattern(
            "نجمة المساء (Evening Star)",
            "evening_star",
            "#ef4444",
            "نمط من ثلاث شموع: شمعة صاعدة كبيرة، شمعة صغيرة (دوجي)، ثم شمعة هابطة كبيرة. إشارة انعكاس قوية جداً",
            "عند إغلاق الشمعة الهابطة الثالثة",
            "مستوى الدعم القوي أو 2:1 من نقطة الدخول",
            "أعلى قمة النمط الكامل"
        )
        
        self.c.showPage()
        self.y_position = self.height - 2*cm
        
        # 4. ثلاثة غربان سوداء
        self.draw_candle_pattern(
            "ثلاثة غربان سوداء (Three Black Crows)",
            "three_black_crows",
            "#ef4444",
            "ثلاث شموع هابطة متتالية بأجسام كبيرة وظلال قصيرة. كل شمعة تفتح داخل جسم الشمعة السابقة وتغلق أسفل منها",
            "بعد إغلاق الشمعة الثالثة",
            "الدعم التالي أو 2:1 من نقطة الدخول",
            "أعلى قمة الشمعة الأولى"
        )
        
        # 5. الغيمة السوداء
        self.draw_candle_pattern(
            "الغيمة السوداء (Dark Cloud Cover)",
            "dark_cloud",
            "#ef4444",
            "شمعة هابطة تفتح أعلى إغلاق الشمعة الصاعدة السابقة وتغلق تحت منتصفها. إشارة انعكاس هابط",
            "عند إغلاق الشمعة الهابطة",
            "مستوى الدعم أو 1.5:1 من نقطة الدخول",
            "أعلى قمة الشمعة الهابطة"
        )
        
        # 6. قمة الملقط
        self.draw_candle_pattern(
            "قمة الملقط (Tweezer Top)",
            "tweezer_top",
            "#ef4444",
            "شمعتان متتاليتان بنفس القمة تقريباً. الأولى صاعدة والثانية هابطة. تشير إلى مقاومة قوية ومحتمل انعكاس هابط",
            "عند كسر أسفل الشمعة الثانية",
            "الدعم التالي أو 1.5:1 من نقطة الدخول",
            "أعلى القمة المشتركة"
        )
        
        self.c.showPage()
        
        # شمعة الدوجي (محايدة)
        self.y_position = self.height - 2*cm
        self.draw_title("شمعة الدوجي (Doji) ⚪", 18)
        self.draw_subtitle("إشارة تردد وعدم حسم", 14)
        self.y_position -= 0.5*cm
        
        self.draw_candle_pattern(
            "الدوجي (Doji)",
            "doji",
            "#9ca3af",
            "شمعة بجسم صغير جداً أو معدوم، سعر الافتتاح يساوي الإغلاق تقريباً. تشير إلى تردد السوق وتوازن بين البائعين والمشترين",
            "انتظر تأكيد الاتجاه من الشمعة التالية",
            "حسب اتجاه الشمعة التالية",
            "حسب اتجاه الشمعة التالية"
        )
        
        self.c.showPage()
        
        # نصائح مهمة
        self.y_position = self.height - 2*cm
        self.draw_title("نصائح مهمة للتداول الناجح", 18)
        self.y_position -= 0.5*cm
        
        tips = [
            "1. التأكيد: لا تدخل صفقة بناءً على شمعة واحدة فقط. انتظر التأكيد من الشمعة التالية.",
            "",
            "2. الإطار الزمني: أنماط الشموع على الإطارات الزمنية الأكبر (4 ساعات، يومي) أكثر موثوقية.",
            "",
            "3. الحجم: تحقق من حجم التداول. الأنماط مع حجم تداول عالي أكثر قوة.",
            "",
            "4. السياق: انظر إلى الاتجاه العام. الأنماط الانعكاسية أقوى عند مستويات الدعم والمقاومة.",
            "",
            "5. إدارة المخاطر: لا تخاطر بأكثر من 1-2% من رأس المال في صفقة واحدة.",
            "",
            "6. نسبة المخاطرة للعائد: استهدف نسبة 1:2 على الأقل (إذا خاطرت ب 10$، استهدف ربح 20$).",
            "",
            "7. Stop Loss: ضع دائماً أمر وقف الخسارة قبل الدخول في الصفقة.",
            "",
            "8. Take Profit: حدد مستويات جني الأرباح مسبقاً ولا تكن طماعاً.",
            "",
            "9. التدريب: تدرب على حساب تجريبي قبل التداول بأموال حقيقية.",
            "",
            "10. الانضباط: التزم بخطتك ولا تدع العواطف تتحكم في قراراتك.",
        ]
        
        for tip in tips:
            self.draw_text(tip, font_size=11, align='center')
        
        self.c.showPage()
        
        # صفحة الخاتمة
        self.y_position = self.height - 2*cm
        self.draw_title("خاتمة", 18)
        self.y_position -= 1*cm
        
        conclusion = [
            "الشموع اليابانية هي أداة قوية ولكنها ليست معصومة من الخطأ.",
            "استخدمها مع أدوات التحليل الفني الأخرى مثل:",
            "• مستويات الدعم والمقاومة",
            "• المؤشرات الفنية (RSI, MACD, Moving Averages)",
            "• خطوط الاتجاه",
            "• أنماط الرسم البياني",
            "",
            "تذكر: التداول الناجح يتطلب:",
            "✓ المعرفة والتعلم المستمر",
            "✓ الصبر والانضباط",
            "✓ إدارة المخاطر الصارمة",
            "✓ التحكم في العواطف",
            "✓ خطة تداول واضحة",
            "",
            "بالتوفيق في رحلتك في عالم التداول! 🏆",
        ]
        
        for text in conclusion:
            self.draw_text(text, font_size=12, align='center')
        
        self.y_position -= 2*cm
        self.c.setFont("Helvetica-Bold", 10)
        self.c.setFillColor(colors.HexColor("#666666"))
        footer = self.arabic_text("© 2025 - دليل الشموع اليابانية للمحترفين")
        text_width = self.c.stringWidth(footer, "Helvetica-Bold", 10)
        self.c.drawString((self.width - text_width) / 2, self.y_position, footer)
        
        # حفظ الملف
        self.c.save()
        print(f"✅ تم إنشاء الملف بنجاح: {self.filename}")

# إنشاء الدليل
if __name__ == "__main__":
    pdf = TradingGuidePDF("دليل_الشموع_اليابانية_للمحترفين.pdf")
    pdf.create_guide()
    print("\n🎉 تم إنشاء دليل الشموع اليابانية بنجاح!")
    print("📄 الملف: دليل_الشموع_اليابانية_للمحترفين.pdf")
