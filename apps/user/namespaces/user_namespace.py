import os
from flask import redirect, render_template, Response, url_for, request
from flask_restx import Namespace, fields, Resource
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from apps.user.forms import RegistrationForm, LoginForm
from apps.user.service import user_service
from apps.user.namespaces import user_namespace
from apps import celery, configuration, login_manager
from utils.http_status import HttpStatus
from utils.blog_logger import BlogLogger
from utils.token import TokenHelper


user_namespace = Namespace('user', description='User Related Namespace')


register_post_response_model = user_namespace.model('Register', {
        'username': fields.String(required=True, 
                              description='Username',
                              example = 'dilipsharma',
                              min_length = 5,
                              max_length = 15
                        ),
        'email': fields.String(required=True, 
                              description='Email of user',
                              example = 'dilipblr25@gmail.com',
                              min_length = 10,
                              max_length = 30
                        ),
    }
)

reg_post_req_parser = user_namespace.parser()
reg_post_req_parser.add_argument('username', type=str, help='Username', location='form')
reg_post_req_parser.add_argument('email', type=str, help='Email', location='form')

login_get_res_model = user_namespace.model('Login', {
        'email': fields.String(required=True, 
                              description='Email of user',
                              example = 'dilipblr25@gmail.com',
                              min_length = 10,
                              max_length = 30
                        ),
        'password': fields.String(required=True, 
                              description='Password',
                              example = 'dl3888c*&Y',
                              min_length = 5,
                              max_length = 15
                        ),
    }
)

login_post_req_parser = user_namespace.parser()
login_post_req_parser.add_argument('email', type=str, help='Email', location='form')
login_post_req_parser.add_argument('password', type=str, help='Password', location='form')

@user_namespace.route("/")
class Home(Resource):
    def get(self):
        return Response(response=render_template('home.html'))

@user_namespace.route("/register")
class Register(Resource):
    @user_namespace.expect(reg_post_req_parser, validate = True)
    def post(self):
        form = RegistrationForm()

        username = form.username.data
        email = form.email.data

        is_success, message, password = user_service.sign_up(username, email)

        if not is_success:
            return {'msg': message}, HttpStatus.HTTP_400_BAD_REQUEST

        # User is created, now generate email token for the user
        token_helper = TokenHelper()

        BlogLogger.get_instance().log_info(f"Generating confirmation token.")
        is_success, message, token = token_helper.generate_confirmation_token(email=email)

        confirm_url = url_for('api.user_verify', token=token, _external=True)

        html_template = render_template(
                'verification.html', 
                username = username, 
                email = email,
                password = password,
                confirm_url=confirm_url
            )

        subject = "Please verify your email"

        BlogLogger.get_instance().log_info(f"Sending email to {email}.")

        # celery.send_task('email.send', (configuration.MAIL_DEFAULT_SENDER, email, subject, html_template))

        # Also write mail template to text file temporarily, this should be removed later
        file_path = os.path.abspath(os.path.dirname(__name__))

        file_name = os.path.join(file_path, 'verification_email.txt')

        BlogLogger.get_instance().log_debug(f"Writing verification email template to file {file_name}.")

        lines = [
                    f"Username is {username}\n",
                    f"Email is {email}\n",
                    f"Password is {password}\n",
            ]
        with open(file=file_name, mode='w') as f:
            f.writelines(lines)

        # headers = {'Content-Type': 'text/html'}
        # return make_response(render_template('index.html'),200,headers)

        return redirect(url_for('api.user_login'))
    
    @user_namespace.response(
        code=HttpStatus.HTTP_200_OK,
        description="Response",
        model=register_post_response_model,
    )
    def get(self):
        form = RegistrationForm()
        return Response(response=render_template('register.html', form=form))

@user_namespace.route('/<token>')
@user_namespace.doc(params={'token': 'Token ID'})
class Verify(Resource):
    def get(self):
        return {'Msg:': 'Verification is Done'}, 200
    
@user_namespace.route("/login")
class Login(Resource):
    @user_namespace.expect(login_post_req_parser, validate = True)
    def post(self):
        if current_user.is_authenticated:
            BlogLogger.get_instance().log_info(f"User is already authenticated.")
            return redirect(url_for('api.user_post_login'))

        form = LoginForm()

        email = form.email.data
        password = form.password.data

        is_success, message, user = user_service.sign_in(email, password)

        if not is_success:
            BlogLogger.get_instance().log_info(f"Failed to login. {message}.")
            return {'msg': message}, HttpStatus.HTTP_400_BAD_REQUEST

        BlogLogger.get_instance().log_info(f"Logging in user.")
        login_user(user)

        next_page = request.args.get('next')

        # if not next_page or url_parse(next_page).netloc != '':
        return redirect(url_for('api.user_post_login'))
        
        # return redirect(next_page)
        # headers = {'Content-Type': 'text/html'}
        # return make_response(render_template('index.html'),200,headers)
    
    @user_namespace.response(
        code=HttpStatus.HTTP_200_OK,
        description="Response",
        model=login_get_res_model,
    )
    def get(self):
        form = LoginForm()
        return Response(response=render_template('login.html', form=form))

@user_namespace.route('/logout')
class Logout(Resource):
    def get(self):
        logout_user()
        return redirect(url_for('api.user_home'))

@user_namespace.route('/post_login')
class PostLogin(Resource):
    decorators = [login_required]
    def get(self):
        return render_template('post_login.html')
    
# @user_namespace.route('/user_loader')
# class UserLoader(Resource):
#     decorators = [login_manager.user_loader]
#     def get(self):
#         is_success, message, user = user_service.load_user(id=id)
#         return user
    
@login_manager.user_loader
def user_loader(id):
    is_success, message, user = user_service.load_user(id=id)
    return user