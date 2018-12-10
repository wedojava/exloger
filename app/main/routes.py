from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, current_app, session
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.main.forms import EditProfileForm, SearchForm
from app.models import User, LogImported
from app.main import bp
from sqlalchemy import and_

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    
    session['email'] = session['email'] if session['email'] else 'example@example.com'
    session['ip'] = session['ip'] if session['ip'] else '127.0.0.1'

    # g.locale = str(get_locale())
    # It's bug for china,I have to set this way. Also, you can set it into base.html
    g.locale = 'zh_CN' if str(get_locale()).startswith('zh') else str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        flash('Search for {}'.format(form.email.data))
        words_email = ["%" + form.email.data + "%"]
        rule_sender = and_(*[LogImported.sender_address.like(w) for w in words_email])
        rule_recipient = and_(*[LogImported.recipient_address.like(w) for w in words_email])
        rule_return = and_(*[LogImported.return_path.like(w) for w in words_email])
        rule_email = rule_sender + rule_recipient + rule_return
        words_ip = ["%" + form.ip.data + "%"]
        rule_client_ip = and_(*[LogImported.client_ip.like(w) for w in words_ip])
        rule_server_ip = and_(*[LogImported.server_ip.like(w) for w in words_ip])
        rule_original_client_ip = and_(*[LogImported.original_client_ip.like(w) for w in words_ip])
        rule_original_server_ip = and_(*[LogImported.original_server_ip.like(w) for w in words_ip])
        rule_ip = rule_client_ip + rule_server_ip + rule_original_client_ip + rule_original_server_ip
        rule = rule_email + rule_ip
        l = LogImported.query.filter(rule)
        # l = LogImported.query.filter(LogImported.sender_address.like("%" + form.email.data + "%")).all()
        # l = LogImported.query.filter_by(sender_address=form.email.data).all()
        flash(l.paginate(page, per_page=50, error_out=True))
        pagination = l.paginate(page, per_page=50, error_out=True)
        pageitems = pagination.items
        session['email'] = form.email.data
        session['ip'] = form.ip.data
        return render_template('index.html', title=_('Home'), form=form, loglist = l, \
        pageitems = pageitems, pagination = pagination)

    elif session['email'] is not 'example@example.com':
        words_email = ["%" + session['email'] + "%"]
        rule_sender = and_(*[LogImported.sender_address.like(w) for w in words_email])
        rule_recipient = and_(*[LogImported.recipient_address.like(w) for w in words_email])
        rule_return = and_(*[LogImported.return_path.like(w) for w in words_email])
        rule_email = rule_sender + rule_recipient + rule_return
        words_ip = ["%" + session['ip'] + "%"]
        rule_client_ip = and_(*[LogImported.client_ip.like(w) for w in words_ip])
        rule_server_ip = and_(*[LogImported.server_ip.like(w) for w in words_ip])
        rule_original_client_ip = and_(*[LogImported.original_client_ip.like(w) for w in words_ip])
        rule_original_server_ip = and_(*[LogImported.original_server_ip.like(w) for w in words_ip])
        rule_ip = rule_client_ip + rule_server_ip + rule_original_client_ip + rule_original_server_ip
        rule = rule_email + rule_ip
        l = LogImported.query.filter(rule)
        flash(l.paginate(page, per_page=50, error_out=True))
        pagination = l.paginate(page, per_page=50, error_out=True)
        pageitems = pagination.items
        return render_template('index.html', title=_('Home'), form=form, loglist = l, \
        pageitems = pageitems, pagination = pagination)
    else:
        return render_template('index.html', title=_('Home'), form=form)
    

 

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)



@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)