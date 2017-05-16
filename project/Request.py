from issue_repository import get_full_stat


class Request(object):
    def __init__(self, server):
        super(Request, self).__init__()
        self._server = server

    def execute(self, name):
        user = self._server.search_users(name)[0]

        periods = 12
        period_len_days = 30

        user_stat_by_period = []
        for period in xrange(periods):

            user_stat_by_period.append(get_full_stat(self._server, user,
                                                     during=period_len_days,
                                                     since_days_back=period * period_len_days))
        return user_stat_by_period

