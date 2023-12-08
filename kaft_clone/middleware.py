import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

SESSION_EXPIRATION_TIME = 30  # dakika cinsinden

def session_check_middleware(get_response):
    def middleware(request):
        if not request.session.session_key or 'last_activity' not in request.session:
            request.session.save()
            request.session['last_activity'] = datetime.now().timestamp()
        else:
            last_activity_time = datetime.fromtimestamp(request.session['last_activity'])
            if datetime.now() - last_activity_time > timedelta(minutes=SESSION_EXPIRATION_TIME):
                request.session.flush()
            else:
                request.session['last_activity'] = datetime.now().timestamp()

        logger.info(f"SESSION KEY: {request.session.session_key}")

        response = get_response(request)

        if hasattr(request, 'context_data'):
            request.context_data['session_key'] = request.session.session_key

        return response

    return middleware
