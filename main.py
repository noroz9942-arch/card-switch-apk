import json
import urllib.request
import threading

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock


class CardSwitchApp(App):
    def build(self):
        self.selected_channels = set()
        self.card_owner_name = ""

        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # عنوان
        title = Label(
            text="[b]سامانه مدیریت و تخصیص تراکنش کارت[/b]",
            markup=True,
            font_size='20sp',
            size_hint_y=None,
            height=40
        )
        main_layout.add_widget(title)

        # بخش استعلام کارت
        card_box = BoxLayout(orientation='horizontal', spacing=5, size_hint_y=None, height=45)
        self.card_input = TextInput(
            hint_text="شماره کارت ۱۶ رقمی را وارد کنید",
            multiline=False,
            input_filter='int'
        )
        inquiry_btn = Button(
            text="استعلام کارت",
            size_hint_x=0.35,
            background_color=(0.2, 0.6, 1, 1)
        )
        inquiry_btn.bind(on_press=self.start_inquiry_thread)

        card_box.add_widget(self.card_input)
        card_box.add_widget(inquiry_btn)
        main_layout.add_widget(card_box)

        # نمایش صاحب کارت
        self.owner_label = Label(
            text="صاحب کارت: ---",
            font_size='14sp',
            size_hint_y=None,
            height=30,
            color=(0.8, 0.8, 0.8, 1)
        )
        main_layout.add_widget(self.owner_label)

        # بخش مبلغ
        amount_box = BoxLayout(orientation='horizontal', spacing=5, size_hint_y=None, height=45)
        amount_label = Label(text="مبلغ (ریال):", size_hint_x=0.3)
        self.amount_input = TextInput(
            hint_text="مبلغ مورد نظر را وارد کنید",
            multiline=False,
            input_filter='int'
        )
        amount_box.add_widget(amount_label)
        amount_box.add_widget(self.amount_input)
        main_layout.add_widget(amount_box)

        # انتخاب کانال‌ها
        channels_title = Label(
            text="[b]انتخاب کانال‌های فعالسازی:[/b]",
            markup=True,
            size_hint_y=None,
            height=30
        )
        main_layout.add_widget(channels_title)

        channels_grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=100)

        channels = [
            ("ATM (خودپرداز)", "ATM"),
            ("POS (کارتخوان)", "POS"),
            ("اینترنت بانک", "INTERNET_BANK"),
            ("USSD (کددستوری)", "USSD")
        ]

        for label_text, channel_key in channels:
            item_box = BoxLayout(orientation='horizontal', spacing=5)
            chk = CheckBox(active=False, size_hint_x=0.3)
            chk.bind(active=lambda instance, value, key=channel_key: self.on_checkbox_active(key, value))
            lbl = Label(text=label_text, halign='left')
            item_box.add_widget(chk)
            item_box.add_widget(lbl)
            channels_grid.add_widget(item_box)

        main_layout.add_widget(channels_grid)

        # بخش لاگ
        self.log_label = Label(
            text="آماده دریافت اطلاعات...\n",
            size_hint_y=None,
            font_size='13sp',
            halign='left',
            valign='top'
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        scroll = ScrollView(size_hint_y=0.4)
        scroll.add_widget(self.log_label)
        main_layout.add_widget(scroll)

        # دکمه Confirm
        self.confirm_btn = Button(
            text="CONFIRM (تأیید و اعمال)",
            size_hint_y=None,
            height=55,
            background_color=(0, 0.8, 0.3, 1),
            font_size='16sp'
        )
        self.confirm_btn.bind(on_press=self.execute_confirmation)
        main_layout.add_widget(self.confirm_btn)

        return main_layout

    def on_checkbox_active(self, channel_key, is_active):
        if is_active:
            self.selected_channels.add(channel_key)
        else:
            self.selected_channels.discard(channel_key)

    def log(self, message):
        Clock.schedule_once(lambda dt: setattr(self.log_label, 'text', self.log_label.text + f"\n{message}"))

    def start_inquiry_thread(self, instance):
        card_num = self.card_input.text.strip()
        if len(card_num) < 16:
            self.log("❌ خطا: شماره کارت باید حداقل ۱۶ رقم باشد.")
            return

        self.log("⏳ در حال استعلام اطلاعات کارت از API...")
        threading.Thread(target=self.call_inquiry_api, args=(card_num,), daemon=True).start()

    def call_inquiry_api(self, card_num):
        url = "https://apim.pishgaman.ir/card/v1/inquiry"
        bearer_token = "Bearer ZMwYuEg6VjSD77eegSoRBpXebAelTcsZG0HhdNMFzC9fJc449tutkmS2BKtVRLTie04uSQ4OMcw8KRuYNSAGzidV7cZ9LZmEec8fgApdjOo="

        headers = {
            "Authorization": bearer_token,
            "Content-Type": "application/json"
        }

        payload = json.dumps({"pan": card_num}).encode('utf-8')

        try:
            req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=10) as response:
                res_data = response.read().decode('utf-8')
                res_json = json.loads(res_data)

                name = res_json.get("name") or res_json.get("result", {}).get("owner", "دارنده کارت شناسایی شد")
                self.card_owner_name = name
                Clock.schedule_once(lambda dt: setattr(self.owner_label, 'text', f"صاحب کارت: {name}"))
                self.log(f"✅ استعلام موفق: {name}")

        except Exception as e:
            fallback_name = "دارنده کارت (نمایشی)"
            self.card_owner_name = fallback_name
            Clock.schedule_once(lambda dt: setattr(self.owner_label, 'text', f"صاحب کارت: {fallback_name}"))
            self.log(f"⚠️ استعلام با خطای شبکه مواجه شد. حالت نمادین فعال گردید.")

    def execute_confirmation(self, instance):
        card_num = self.card_input.text.strip()
        amount = self.amount_input.text.strip()

        if not card_num:
            self.log("❌ خطا: لطفا شماره کارت را وارد کنید.")
            return
        if not amount:
            self.log("❌ خطا: لطفا مبلغ را وارد کنید.")
            return
        if not self.selected_channels:
            self.log("❌ خطا: حداقل یک کانال را انتخاب کنید.")
            return

        formatted_amount = "{:,}".format(int(amount))
        selected_list = ", ".join(list(self.selected_channels))

        summary = (
            f"\n========================================\n"
            f"✅ تراکنش نمایشی با موفقیت ثبت شد:\n"
            f"💳 کارت: {card_num}\n"
            f"👤 نام: {self.card_owner_name if self.card_owner_name else 'تأیید شده'}\n"
            f"💰 مبلغ تخصیص یافته: {formatted_amount} ریال\n"
            f"🌐 کانال‌های فعال: [{selected_list}]\n"
            f"========================================"
        )
        self.log(summary)


if __name__ == '__main__':
    CardSwitchApp().run()