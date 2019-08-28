from flask import render_template, request, Blueprint
from core.models import Post
from core.posts.forms import SearchForm

# 'main' will be the name of the blueprint
main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    search = SearchForm()
    page = request.args.get('page', 1, type=int) # 1 is the default page number
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, form=search)


@main.route("/about")
def about():
    return render_template('about.html', title="About")

