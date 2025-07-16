with calendar as (
  select
    generate_series(
      date_trunc('day', current_date - interval '90 days'),
      date_trunc('day', current_date + interval '30 days'),
      interval '1 day'
    )::date as date_day
)

select
  date_day,
  extract(year from date_day)::int as year,
  extract(month from date_day)::int as month,
  extract(day from date_day)::int as day,
  to_char(date_day, 'Day') as weekday
from calendar
