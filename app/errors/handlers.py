from flask import render_template, current_app

from app import db
from app.errors import bp


@bp.app_errorhandler(400)
@bp.app_errorhandler(401)
@bp.app_errorhandler(403)
@bp.app_errorhandler(404)
@bp.app_errorhandler(405)
@bp.app_errorhandler(406)
@bp.app_errorhandler(408)
@bp.app_errorhandler(409)
@bp.app_errorhandler(410)
@bp.app_errorhandler(411)
@bp.app_errorhandler(412)
@bp.app_errorhandler(413)
@bp.app_errorhandler(414)
@bp.app_errorhandler(415)
@bp.app_errorhandler(416)
@bp.app_errorhandler(417)
@bp.app_errorhandler(418)
@bp.app_errorhandler(422)
@bp.app_errorhandler(423)
@bp.app_errorhandler(424)
@bp.app_errorhandler(428)
@bp.app_errorhandler(429)
@bp.app_errorhandler(431)
def general_error(error):  # 400 error handler
    return render_template('errors/error.html', error=error, error_code=error.code, error_name=error.name,
                           error_description=error.description), error.code


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    current_app.logger.critical(f'Internal Error occurred - database was rolled back for safety')
    return render_template('errors/error.html', error=error, error_code=500), 500
