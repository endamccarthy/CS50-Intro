from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    # In flask we can pass in an error code with the render template. 
    # This is default set at 200 so we never needed to actually write it before.
    if error.description:
        response = {'message': error.description}
        return render_template('errors/404.html', response=response), 404
    else:
        return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500

