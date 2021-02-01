from account.constants.account import BASE_CURRENCY
from datetime import datetime
from django.contrib.sessions.models import Session
from django.db import connection
from moneyed import Money


class DashboardController(object):
    """
    Base dashboard mixin that defines some default content that is present on
    every dashboard tab.
    """

    DISPLAY_MONTHS = 5
    DISPLAY_DAYS = 7
    ACTIVE_WEEKS = 26
    MONTHS_AVERAGE = 12

    @staticmethod
    def active_users():
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT count(*) AS users
                FROM base_user
                WHERE is_superuser = false AND is_staff = false AND last_name NOT IN('Demo', 'System') AND
                    last_login >= current_date - interval '%s weeks'
            ;"""
            % DashboardController.ACTIVE_WEEKS
        )
        rows = cursor.fetchall()
        value = rows[0][0]
        return value

    @staticmethod
    def total_users():
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT count(*) AS users
                FROM base_user
                WHERE is_superuser = false AND is_staff = false AND last_name NOT IN('Demo', 'System')
            ;"""
        )
        rows = cursor.fetchall()
        value = rows[0][0]
        return value

    @staticmethod
    def online_users():
        return Session.objects.filter(expire_date__gte=datetime.now()).count()

    @staticmethod
    def current_liability():
        cursor = connection.cursor()
        cursor.execute(
            """
            select sum(balance) as liability
            from account_account
            where internal_type_id in (3,4) and accounting_type = 'LIABILITY'
            ;"""
        )
        rows = cursor.fetchall()
        value = Money(rows[0][0], BASE_CURRENCY)
        return value

    @staticmethod
    def active_deals():
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT count(*) as Transactions
                FROM vault_deal
                WHERE state NOT IN('CLOSED', 'CREATE', 'PENDING', 'CANCELLED')
            ;"""
        )
        rows = cursor.fetchall()
        value = rows[0][0]
        return value

    @staticmethod
    def user_sign_ups():
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT CASE WHEN Period_Type = 'Year' THEN
                        (CASE WHEN date_part('year', current_date) = date_part('year', period) THEN 'This year'
                        WHEN date_part('year', current_date) - date_part('year', period) = 1 THEN 'Last year'
                        ELSE to_char(date_part('year', period),'9999') END)
                    WHEN Period_Type = 'Month' THEN
                        (CASE WHEN date_part('year', current_date) = date_part('year', period) AND
                            date_part('month', current_date) = date_part('month', period) THEN 'This month'
                        ELSE to_char(to_timestamp(to_char(date_part('month', period), '999'), 'MM'), 'Mon')||' '||
                        to_char(date_part('year', period),'9999')
                        END)
                    ELSE
                        (CASE WHEN current_date = Period THEN 'Today'
                        ELSE to_char(current_date - Period,'99') || ' days ago'
                        END)
                    END AS Heading,
                    period_type, period, users, coalesce(new_users,0) AS new_users, days, coalesce(new_users,0)/CASE WHEN days = 0 THEN 1 ELSE days END AS Avg_New_Daily
            FROM (
                SELECT 'Day' AS period_type, date_trunc AS period, count(b.*) AS Users, New_Users,1 AS Days
                FROM 	(
                    SELECT date_trunc('day', dd):: date
                    FROM generate_series
                    ( '2014-06-01'::timestamp , current_date::timestamp , '1 day'::interval) dd
                    ) a
                LEFT JOIN base_user b ON last_login >= date_trunc - interval '%s weeks' AND date_joined <= date_trunc + interval '1 day'
                LEFT JOIN (
                    SELECT  date(date_joined) AS Period,count(*) as New_Users
                    FROM base_user
                    WHERE is_superuser = false AND is_staff = false AND last_name NOT IN('Demo', 'System')
                    GROUP BY date(date_joined)
                        ) c ON a.date_trunc = c.period
                WHERE b.is_superuser = false AND b.is_staff = false AND b.last_name NOT IN('Demo', 'System') AND
                    date_trunc >= current_date - interval '%s days'
                GROUP BY a.date_trunc, c.new_users

                UNION ALL

                SELECT 'Month' AS period_type, date_trunc AS period, count(b.*) AS Users, New_Users,
			            CASE WHEN extract(year from age(date_trunc)) = 0 AND extract(month from date_trunc) = date_part('month', current_date)
                             THEN current_date - to_date(to_char(date_part('year', date_trunc),'9999') || '-' || to_char(date_part('month', date_trunc),'99') ||'-01','YYYY-mm-dd')
                             ELSE date_part('days', DATE_TRUNC('month', date_trunc) + '1 MONTH'::INTERVAL - '1 day'::interval)
                             END AS Days
                FROM 	(
                    SELECT date_trunc('day', dd):: date
                    FROM generate_series
                    ( '2014-01-01'::timestamp , current_date::timestamp , '1 month'::interval) dd
                    ) a
                LEFT JOIN base_user b ON last_login >= date_trunc - interval '%s weeks' AND date_joined <= date_trunc + interval '1 month'
                LEFT JOIN (
                    SELECT to_date(to_char(date_part('year', date_joined),'9999')||'-'||to_char(date_part('month', date_joined),'FM99')
                            ||'-01', 'YYYY-MM-DD') as Period,
                        count(*) AS New_Users
                    FROM base_user
                    WHERE Is_superuser = false AND is_staff = false AND last_name NOT IN('Demo', 'System')
                    GROUP BY
                        to_date(to_char(date_part('year', date_joined),'9999')||'-'||to_char(date_part('month', date_joined),'FM99')
                            ||'-01', 'YYYY-MM-DD')
                        ) c ON a.date_trunc = c.period
                WHERE (b.is_superuser = false OR b.is_superuser IS NULL)
                    AND (b.is_staff = false OR b.is_staff IS NULL)
                    AND (b.last_name NOT IN('Demo', 'System') OR b.last_name IS NULL )
                    AND date_trunc >= current_date - interval '%s months'
                GROUP BY date_trunc, c.New_Users

                UNION ALL

                SELECT 'Year' AS period_type, date_trunc AS period, count(B.*) AS Users, New_Users,
			            CASE WHEN date_part('year', current_date) > date_part('year', date_trunc) THEN 365.25
                             ELSE current_date - to_date(to_char(date_part('year', date_trunc),'9999') || '-01-01','YYYY-mm-dd')
                             END AS Days
                FROM 	(
                    SELECT date_trunc('day', dd):: date
                    FROM generate_series
                    ( '2014-01-01'::timestamp , current_date::timestamp , '1 year'::interval) dd
                    ) a
                LEFT JOIN base_user b ON last_login >= date_trunc - interval '%s weeks' AND date_joined <= date_trunc + interval '1 year'
                LEFT JOIN (
                    SELECT to_date(to_char(date_part('year', date_joined),'9999')||'-01-01', 'YYYY-MM-DD') as Period,
                        count(*) AS New_Users
                    FROM base_user
                    WHERE is_superuser = false AND is_staff = false AND last_name NOT IN('Demo', 'System')
                    GROUP BY to_date(to_char(date_part('year', date_joined),'9999')||'-01-01', 'YYYY-MM-DD')
                        ) c ON a.date_trunc = c.period
                WHERE (b.is_superuser = false OR b.is_superuser IS NULL)
                    AND (b.is_staff = false OR b.is_staff IS NULL)
                    AND (b.last_name NOT IN('Demo', 'System') OR b.last_name IS NULL )
                GROUP BY a.date_trunc, c.New_Users
                ) X
            ORDER BY PERIOD, period_type desc
            ;"""
            % (
                DashboardController.ACTIVE_WEEKS,
                DashboardController.DISPLAY_DAYS,
                DashboardController.ACTIVE_WEEKS,
                DashboardController.DISPLAY_MONTHS,
                DashboardController.ACTIVE_WEEKS,
            )
        )
        rows = cursor.fetchall()
        return rows

    @staticmethod
    def liability_balance():
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT  CASE WHEN Period_Type = 'Year' THEN
                        (CASE WHEN date_part('year', current_date) = date_part('year', period) THEN 'This year'
                        WHEN date_part('year', current_date) - date_part('year', period) = 1 THEN 'Last year'
                        ELSE to_char(date_part('year', period),'9999') END)
                    WHEN Period_Type = 'Month' THEN
                        (CASE WHEN date_part('year', current_date) = date_part('year', period) AND
                        date_part('month', current_date) = date_part('month', period) THEN 'This month'
                        ELSE to_char(to_timestamp(to_char(date_part('month', period), '999'), 'MM'), 'Mon')||' '||
                        to_char(date_part('year', period),'9999')
                        END)
                    ELSE
                        (CASE WHEN current_date = Period THEN 'Today'
                        ELSE to_char(current_date - Period,'99') || ' days ago'
                        END)
                    END AS Heading,
                    Period_type, Period, COALESCE(Opening_balance,0) AS Opening_Bal
            FROM (
                SELECT 'Year' AS Period_Type, Year AS Period, sum(account_balance) AS Opening_Balance
                FROM    (
                            SELECT date_trunc AS Year, id, max(PayID) as PayID
                            FROM    (
                                        SELECT date_trunc('day', dd):: date
                                        FROM generate_series
                                        ( '2014-01-01'::timestamp
                                        , (current_date + interval '1 year')::timestamp
                                        , '1 year'::interval) dd
                                    ) F
                            LEFT JOIN   (
                                            SELECT id, max(PayID) AS PayID, year
                                            FROM (
                                                    SELECT A.id, B.id AS PayID,
                                                            to_date(to_char(date_part('year', B.date_created)+1,'9999')||'-01-01', 'YYYY-MM-DD') AS Year
                                                    FROM account_account A
                                                    JOIN account_journalentryline B ON A.id = B.account_id
                                                    WHERE internal_type_id IN (3,4) AND accounting_type = 'LIABILITY'
                                                ) Caccount_journalentryline
                                            GROUP BY id, year
                                        ) G
                            ON F.date_trunc >= year
                            GROUP BY date_trunc, id
                        ) H
                LEFT JOIN account_journalentryline I ON I.id = H.payid
                GROUP BY year
                HAVING year <= current_date

                UNION ALL

                SELECT 'Month' AS Period_Type, Month AS Period, sum(account_balance) AS Opening_Balance
                FROM    (
                            SELECT date_trunc AS Month, id, max(PayID) as PayID
                            FROM    (
                                        SELECT date_trunc('day', dd):: date
                                        FROM generate_series
                                        ( '2014-01-01'::timestamp
                                        , (current_date + interval '1 month')::timestamp
                                        , '1 month'::interval) dd
                                    ) F
                            LEFT JOIN   (
                                            SELECT id, max(PayID) AS PayID, month
                                            FROM    (
                                                        SELECT A.id, B.id AS PayID,
                                                        to_date(to_char(date_part('year', B.date_created),'9999')||'-'||to_char(date_part('month', B.date_created)+1,'FM99')
                                                        ||'-01', 'YYYY-MM-DD') AS Month
                                                        FROM account_account A
                                                        JOIN account_journalentryline B ON A.id = B.account_id
                                                        WHERE internal_type_id IN (3,4) AND accounting_type = 'LIABILITY'
                                                    ) C
                                            GROUP BY id, month
                                        ) G
                            ON F.date_trunc >= Month
                            GROUP BY date_trunc, id
                        ) H
                LEFT JOIN account_journalentryline I ON I.id = H.payid
                GROUP BY month
                HAVING month >= (current_date - interval '%s month')::date and month <= current_date

                UNION ALL

                SELECT 'Day' AS Period_Type, Day AS Period, sum(account_balance) AS Opening_Balance
                FROM    (
                            SELECT date_trunc AS Day, id, max(PayID) AS PayID
                            FROM    (
                                        SELECT date_trunc('day', dd):: date
                                        FROM generate_series
                                        ( '2014-06-01'::timestamp
                                        , (current_date)::timestamp
                                        , '1 day'::interval) dd
                                    ) F
                            LEFT JOIN   (
                                            SELECT id, max(PayID) AS PayID, Day
                                            FROM    (
                                                        SELECT A.id, B.id AS PayID,
                                                        to_date(to_char(date_part('year', B.date_created),'9999')||'-'||to_char(date_part('month', B.date_created),'FM99')
                                                        ||'-'||to_char(date_part('day', B.date_created)+1,'FM99'), 'YYYY-MM-DD') AS Day
                                                        FROM account_account A
                                                        JOIN account_journalentryline B ON A.id = B.account_id
                                                        WHERE internal_type_id in (3,4) AND accounting_type = 'LIABILITY'
                                                    ) C
                                            GROUP BY id, Day
                                        ) G
                            ON F.date_trunc >= Day
                            GROUP BY date_trunc, id
                        ) H
                LEFT JOIN account_journalentryline I ON I.id = H.payid
                GROUP BY Day
                HAVING Day >= (current_date - interval '%s day')::date
                ) X
            ORDER BY Period, period_type asc
            ;"""
            % (
                DashboardController.DISPLAY_MONTHS,
                DashboardController.DISPLAY_DAYS,
            )
        )
        rows = cursor.fetchall()

        # Convert money fields
        size = len(rows)
        count = 0

        while count < size:
            row = list(rows[count])
            row.append(row[3])
            row[3] = str(Money(row[3], BASE_CURRENCY))
            rows[count] = row
            count += 1
        return rows

    @staticmethod
    def deal_states():
        cursor = connection.cursor()
        cursor.execute(
            "SELECT state as Status, count(*) as Transactions "
            "FROM vault_deal "
            "GROUP BY state "
            "ORDER BY state;"
        )
        rows = cursor.fetchall()
        return rows

    @staticmethod
    def avg_trans():
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT count(*) AS transactions, avg(value) AS avg_value, avg(fee) as avg_fee
                FROM vault_deal
                WHERE start_date >= current_date - interval '%s months'
                    AND id in(  SELECT distinct deal_id
                                FROM notifications_notification
                                WHERE subject = 'Transaction Activated')
            ;"""
            % DashboardController.MONTHS_AVERAGE
        )
        rows = cursor.fetchall()

        # Convert money fields
        size = len(rows)
        count = 0

        while count < size:
            row = list(rows[count])
            if row[1]:
                row[1] = str(Money(row[1], BASE_CURRENCY))
            if row[2]:
                row[2] = str(Money(row[2], BASE_CURRENCY))
            rows[count] = row
            count += 1
        return rows

    @staticmethod
    def trans_duration():
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT	count(*) AS Transactions, round(avg(Days_to_Open),1) AS Days_to_Open, round(avg(Days_Open),1) AS Days_Open,
                        round(avg(Total_Days),1) AS Total_Days
                FROM 	(
                        SELECT a.id AS Trans, B.id AS journal, A.Start_date,
                            date(max(C.Date_Created)) AS Open_Date, date(max(B.Date_created)) AS Close_Date,
                            date(max(C.Date_Created))- A.Start_date AS Days_to_Open,
                            date(max(B.Date_created))- date(max(C.Date_Created)) AS Days_Open,
                            date(max(B.Date_created)) - A.Start_date AS Total_Days
                        FROM vault_deal a
                        JOIN account_journalentryline b on a.account_id = b.account_id
                        JOIN notifications_notification c on a.id = c.deal_id
                        WHERE b.id in(	SELECT max(id) AS last_journal
                                FROM account_journalentryline
                                GROUP BY account_id)
                            AND c.subject = 'Transaction Activated'
                            AND B.account_balance = 0
                        GROUP BY a.id, B.id, B.account_balance, A.Start_date
                        ) X
                WHERE	start_date >= current_date - interval '%s months'
            ;"""
            % DashboardController.MONTHS_AVERAGE
        )
        rows = cursor.fetchall()
        return rows

    @staticmethod
    def trans_progress():
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT	count(*) AS Transactions, sum(split) AS splits, sum(refund) AS refunds, sum(payment) AS payments,
                        sum(CASE WHEN payment = 1 AND split = 0 AND refund = 0 THEN 1 ELSE 0 END) AS Single_pay,
                        sum(CASE WHEN payment = 0 AND split = 0 AND refund = 1 THEN 1 ELSE 0 END) AS Single_refund,
                        sum(CASE WHEN payment = 0 AND split = 1 AND refund = 0 THEN 1 ELSE 0 END) AS Single_split,
                        sum(CASE WHEN payment > 1 AND split = 0 AND refund = 0 THEN 1 ELSE 0 END) AS multiple_pay,
                        sum(CASE WHEN payment = 0 AND split = 0 AND refund > 1 THEN 1 ELSE 0 END) AS multiple_refund,
                        max(payment) AS Most_pay
                FROM 	(
                        SELECT a.id AS Trans, a.account_id AS Acc, A.Start_date
                        FROM vault_deal a
                        JOIN account_journalentryline b ON a.account_id = b.account_id
                        JOIN notifications_notification c ON a.id = c.deal_id
                        WHERE b.id in(	SELECT max(id) AS lASt_journal
                                FROM account_journalentryline
                                GROUP BY account_id)
                            AND c.subject = 'Transaction Activated'
                            AND B.account_balance = 0
                        GROUP BY a.id, a.account_id, B.id, B.account_balance, A.Start_date
                        ) X
                JOIN    (SELECT account_id,
                                sum(CASE WHEN refund = payment THEN 1 ELSE 0 END) AS Split,
                                sum(CASE WHEN refund <> payment THEN refund ELSE 0 END) AS Refund,
                                sum(CASE WHEN refund <> payment THEN payment ELSE 0 END) AS Payment
                        FROM (
                                SELECT account_id, date_trunc('minute', date_created) AS date,
                                        sum(CASE WHEN left(description, 6) = 'Refund' THEN 1 ELSE 0 END) AS Refund,
                                        sum(CASE WHEN left(description, 7) = 'Payment' THEN 1 ELSE 0 END) AS Payment
                                FROM account_journalentryline
                                WHERE account_id in(	SELECT distinct a.id
                                                        FROM account_account a
                                                        JOIN account_accounttype b on a.internal_type_id = b.id
                                                        WHERE b.code = 'VAULT')
                                    AND line_type = 'D' AND description not in('Vault Transaction fee', 'Add Money fee')
                                GROUP BY account_id, date_trunc('minute', date_created)
                                ) Y
                        GROUP BY account_id) Z
                        ON Z.account_id = X.acc
                WHERE	start_date >= current_date - interval '%s months'
            """
            % DashboardController.MONTHS_AVERAGE
        )
        rows = cursor.fetchall()

        # Convert money fields
        size = len(rows)
        count = 0

        while count < size:
            row = list(rows[count])
            if row[1] and row[0]:
                row.append(round(100 * row[1] / row[0], 0))
            if row[2] and row[0]:
                row.append(round(100 * row[2] / row[0], 0))
            if row[3] and row[0]:
                row.append(round(100 * row[3] / row[0], 0))
            if row[4] and row[0]:
                row.append(round(100 * row[4] / row[0], 0))
            if row[5] and row[0]:
                row.append(round(100 * row[5] / row[0], 0))
            if row[6] and row[0]:
                row.append(round(100 * row[6] / row[0], 0))
            if row[7] and row[0]:
                row.append(round(100 * row[7] / row[0], 0))
            if row[8] and row[0]:
                row.append(round(100 * row[8] / row[0], 0))
            rows[count] = row
            count += 1
        return rows

    @staticmethod
    def deal_create_metrics():
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT 		CASE WHEN Period_Type = 'Year' THEN
                                (CASE WHEN date_part('year', current_date) = date_part('year', period) THEN 'This year'
                                WHEN date_part('year', current_date) - date_part('year', period) = 1 THEN 'Last year'
                                ELSE to_char(date_part('year', period),'9999') END)
                            WHEN Period_Type = 'Month' THEN
                                (CASE WHEN date_part('year', current_date) = date_part('year', period) AND
                                    date_part('month', current_date) = date_part('month', period) THEN 'This month'
                                ELSE to_char(to_timestamp(to_char(date_part('month', period), '999'), 'MM'), 'Mon')||' '||
                                to_char(date_part('year', period),'9999')
                                END)
                            ELSE
                                (CASE WHEN current_date = Period THEN 'Today'
                                ELSE to_char(current_date - Period,'99') || ' days ago'
                                END)
                            END AS Heading,
                            *,(T.Fees - T.Fees_pENDing - T.Fees_lost) AS Fees_Earned,
                            CASE WHEN T.Fees = 0 THEN 0 ELSE round((T.Fees - T.Fees_pENDing - T.Fees_lost)/T.Fees*100,0) END AS Fees_Rate,
                            CASE WHEN T.days = 0 THEN 0 ELSE T.Transactions/T.days END AS Avg_Trans,
                            CASE WHEN T.days = 0 THEN 0 ELSE T.Value/T.Days END AS Avg_Value,
                            CASE WHEN T.days = 0 THEN 0 ELSE T.Fees/T.Days END AS Avg_Fees,
                            CASE WHEN T.Transactions = 0 THEN 0 else T.Value/T.Transactions END AS AVG_Trans_Val,
                            CASE WHEN T.Transactions = 0 THEN 0 else T.Fees/T.Transactions END AS AVG_Fee_Val
            FROM		(
                    SELECT 'Year' AS Period_Type, date_trunc AS Period,
                            CASE
                                                        WHEN date_part('year', current_date) > date_part('year', date_trunc) THEN 365.25
                                                        ELSE current_date - to_date(to_char(date_part('year', date_trunc),'9999') || '-01-01','YYYY-mm-dd')
                                                    END AS Days,
                            coalesce(Transactions, 0) AS Transactions,
                            coalesce(Value, 0) AS Value,
                            coalesce(Fees, 0) AS Fees,
                            coalesce(Fees_pending, 0) AS Fees_pending,
                            coalesce(Fees_lost, 0) AS Fees_lost
                    FROM (

                            SELECT date_trunc('day', dd):: date
                            FROM generate_series
                            ( '2014-01-01'::timestamp
                            , (current_date)::timestamp
                            , '1 year'::interval) dd
                            ) F
                    LEFT JOIN (
                            SELECT		'Year' AS Period_Type,
                                        to_date((to_char(date_part('year',start_date),'9999')|| ' 01'),'YYYY MM DD') AS Period,
                                        count(*) AS Transactions,
                                        sum(value) AS Value,
                                        sum(fee) AS Fees,
                                        sum(Fees_pending) Fees_pending,
                                        sum(fees_lost) Fees_lost
                            FROM		(SELECT *,
                                        CASE WHEN (state in('CREATE','PENDING')) THEN fee ELSE 0 END Fees_pending,
                                        CASE WHEN (state = 'CLOSED' AND id not in (SELECT distinct deal_id
                                                        FROM notifications_notification
                                                        WHERE subject = 'Transaction Activated') )
                                        THEN fee ELSE 0 END Fees_lost
                                        FROM vault_deal) V
                            GROUP BY	to_date((to_char(date_part('year',start_date),'9999')|| ' 01'),'YYYY MM DD'),
                                        CASE
                                            WHEN date_part('year', current_date) > date_part('year', start_date) THEN 365.25
                                            ELSE current_date - to_date(to_char(date_part('year', start_date),'9999') || '-01-01','YYYY-mm-dd')
                                        END
                            ) X ON F.date_trunc = X.period

                    UNION ALL

                    SELECT 'Month' AS Period_Type, date_trunc AS Period,
                                        CASE
                                            WHEN extract(year FROM age(date_trunc)) = 0 AND extract(month FROM date_trunc) = date_part('month', current_date)
                                            THEN current_date -
                                            to_date(to_char(date_part('year', date_trunc),'9999') || '-' || to_char(date_part('month', date_trunc),'99') ||'-01','YYYY-mm-dd')
                                            ELSE DATE_PART('days', DATE_TRUNC('month', date_trunc) + '1 MONTH'::INTERVAL - '1 day'::interval)
                                        END AS Days ,
                            coalesce(Transactions, 0) AS Transactions,
                            coalesce(Value, 0) AS Value,
                            coalesce(Fees, 0) AS Fees,
                            coalesce(Fees_pending, 0) AS Fees_pending,
                            coalesce(Fees_lost, 0) AS Fees_lost
                    FROM    (
                            SELECT date_trunc('day', dd):: date
                            FROM generate_series
                            ( '2014-01-01'::timestamp
                            , (current_date)::timestamp
                            , '1 Month'::interval) dd
                            ) F
                    LEFT JOIN (
                            SELECT	'Month' as Period_Type,
                                    to_date((to_char(date_part('year',start_date),'9999')|| to_char(date_part('month',start_date),'09')||' 01'),'YYYY MM DD') AS Period,
                                    count(*) AS Transactions,
                                    sum(value) AS Value,
                                    sum(fee) AS Fees,
                                    sum(Fees_pending) Fees_pending,
                                    sum(fees_lost) Fees_lost
                            FROM		(SELECT *,
                                        CASE WHEN (state in('CREATE','PENDING')) THEN fee ELSE 0 END Fees_pending,
                                        CASE WHEN (state = 'CLOSED' AND id not in (SELECT distinct deal_id
                                                        FROM notifications_notification
                                                        WHERE subject = 'Transaction Activated') )
                                        THEN fee ELSE 0 END Fees_lost
                                        FROM vault_deal) V
                            GROUP BY	to_date((to_char(date_part('year',start_date),'9999')|| to_char(date_part('month',start_date),'09')||' 01'),'YYYY MM DD'),
                                        CASE
                                            WHEN extract(year FROM age(start_date)) = 0 AND extract(month FROM start_date) = date_part('month', current_date)
                                            THEN current_date -
                                            to_date(to_char(date_part('year', start_date),'9999') || '-' || to_char(date_part('month', start_date),'99') ||'-01','YYYY-mm-dd')
                                            ELSE DATE_PART('days', DATE_TRUNC('month', start_date) + '1 MONTH'::INTERVAL - '1 day'::interval)
                                        END
                            ) Y ON F.date_trunc = Y.period
                    WHERE		(extract(year FROM age(date_trunc))*12 + extract(month FROM age(date_trunc))) between 0 and %s

                    UNION ALL

                    SELECT 'Days' AS Period_Type, date_trunc AS Period,  1 AS Days ,
                            coalesce(Transactions, 0) AS Transactions,
                            coalesce(Value, 0) AS Value,
                            coalesce(Fees, 0) AS Fees,
                            coalesce(Fees_pending, 0) AS Fees_pending,
                            coalesce(Fees_lost, 0) AS Fees_lost
                    FROM    (
                            SELECT date_trunc('day', dd):: date
                            FROM generate_series
                            ( '2014-01-01'::timestamp
                            , (current_date)::timestamp
                            , '1 day'::interval) dd
                            ) F
                    LEFT JOIN (
                            SELECT	Start_date,
                                        count(*) AS Transactions,
                                        sum(value) AS Value,
                                        sum(fee) AS Fees,
                                        sum(Fees_pENDing) Fees_pENDing,
                                        sum(fees_lost) Fees_lost
                            FROM		(SELECT *,
                                        CASE WHEN (state in('CREATE','PENDING')) THEN fee ELSE 0 END Fees_pENDing,
                                        CASE WHEN (state = 'CLOSED' AND id not in (SELECT distinct deal_id
                                                        FROM notifications_notification
                                                        WHERE subject = 'Transaction Activated') )
                                        THEN fee ELSE 0 END Fees_lost
                                        FROM vault_deal) V
                            GROUP BY	start_date
                            ) Z ON F.date_trunc = Z.Start_date
                    WHERE current_date - date_trunc between 0 and %s
                            ) T
            ORDER BY 	Period, period_type desc
            """
            % (
                DashboardController.DISPLAY_MONTHS - 1,
                DashboardController.DISPLAY_DAYS,
            )
        )
        rows = cursor.fetchall()

        # Convert money fields
        size = len(rows)
        count = 0

        while count < size:
            row = list(rows[count])
            row[5] = str(Money(row[5], BASE_CURRENCY))
            row[6] = str(Money(row[6], BASE_CURRENCY))
            row[9] = str(Money(row[9], BASE_CURRENCY))
            row[14] = str(Money(row[14], BASE_CURRENCY))
            row[15] = str(Money(row[15], BASE_CURRENCY))
            rows[count] = row
            count += 1
        return rows
