from flask import Blueprint, render_template, request, redirect
from data.db_session import create_session
from data.category import Category

blueprint = Blueprint(
    'category_api',
    __name__,
    template_folder='templates')


@blueprint.route('/categories', methods=['GET', 'POST'])
def select_category():
    db_sess = create_session()
    if request.method == 'GET':
        categories = db_sess.query(Category).all()
        return render_template('select_category.html', categories=categories, title='Категории')
    elif request.method == 'POST':
        print(request.form['category'])
        return redirect(f'/categories/{int(request.form["category"])}')
