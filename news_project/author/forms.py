from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, label="Kullanıcı Adı", widget=forms.TextInput(attrs={"class" : "form-control","placeholder" : "Username"}))
    password = forms.CharField(max_length=20, label="Şifre", widget=forms.PasswordInput(attrs={"class" : "form-control","placeholder" : "Password"}))
    password_confirm = forms.CharField(max_length=20, label="Şifre (Tekrar)", widget=forms.PasswordInput(attrs={"class" : "form-control", "placeholder" : "Password"}))

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("password_confirm")

        if password and confirm and password !=confirm:
            raise forms.ValidationError("Şifreler eşleşmiyor.")

        # verileri döndürmek için bir dictionary oluşturmamız gerekiyor.
        values = {
            "username": username,
            "password": password
        }

        return values


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label="Kullanıcı Adı", widget=forms.TextInput(attrs={"class" : "form-control","placeholder" : "Username"}))
    password = forms.CharField(max_length=20, label="Şifre", widget=forms.PasswordInput(attrs={"class" : "form-control","placeholder" : "Password"}))
    # herhangi bir clean metodu yazmadık . Yani bir override yok burada.
    # Bu durumda Inherit aldığımız form class'ında default olarak ne varsa o çalışacak.