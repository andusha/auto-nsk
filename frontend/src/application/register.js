import '../styles/form.scss';

function validation(){
    'use strict';

    password.addEventListener('input', function() {
    this.value != confirmPassword.value ? confirmPassword.setCustomValidity('Password incorrect') : confirmPassword.setCustomValidity('');
    });

    confirmPassword.addEventListener('input', function() {
        this.value != password.value ? this.setCustomValidity('Password incorrect') : this.setCustomValidity('');
        }
    );}
function createForm() {
    'use strict';

    const main = document.querySelector('.main');
    const selection = document.querySelector('.reg-2-type-selection');

    fiz.addEventListener('click', function(){
        selection.remove();

        let div = document.createElement('div');
        div.classList.add('form');
        div.innerHTML = `<form class="register-form" action="/register" method="post">
                                <input type="text" placeholder="name" name="name" id="name" required/>
                                <input type="password" placeholder="password" name="psw" id="password" required/>
                                <input type="password" placeholder="repeat password" name="psw2" id="confirmPassword" required/>
                                <input type="email" placeholder="email address" name="email" id="email" required/>
                                <button type="submit">create</button>
                                <p class="message">Already registered? <a href="{{url_for('login')}}">Sign In</a></p>
                            </form>`;
        main.appendChild(div);
        validation();
    });

    ur.addEventListener('click', function(){
        selection.remove();

        let div = document.createElement('div');
        div.classList.add('form');
        div.innerHTML = `<form class="register-form" action="/register" method="post">
                                <input type="text" placeholder="name" name="name" id="name" required/>
                                <input type="password" placeholder="password" name="psw" id="password" required/>
                                <input type="password" placeholder="repeat password" name="psw2" id="confirmPassword" required/>
                                <input type="email" placeholder="email address" name="email" required/>
                                <hr>
                                <h2 class="org-title">Данные организации</h2>
                                <div class="first-input-row">
                                    <input type="text" name="companyOpf" id="companyOpf" placeholder="ООО" class="first-row-1">
                                    <input type="text" name="companyName" id="companyName" placeholder="Название компании">
                                </div>
                                <div class="second-input-row">
                                    <input type="text" name="companyInn" id="companyInn" placeholder="ИНН*">
                                    <input type="text" name="companyKpp" id="companyKpp" placeholder="КПП*">
                                    <input type="number" name="companyPhone" id="companyPhone" placeholder="Телефон орнанизации">
                                </div>
                                <input type="text" name="companyAddress" id="companyAddress" placeholder="Юридический Адрес">
                                <input type="text" name="companyType" id="companyType" placeholder="Тип Организации">
                                <button type="submit">create</button>
                                <p class="message">Already registered? <a href="{{url_for('login')}}">Sign In</a></p>
                            </form>`;
        main.appendChild(div);
        validation();
    });
}

createForm();