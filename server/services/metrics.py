from services import analytics_service

METRICS = {
    "employees-df": {
        "func": analytics_service.get_employees_df,
        "has_plot": False,
        "title": "All",
        "description": "Возвращает полный список всех сотрудников с их данными"
    },
    "average-experience": {
        "func": analytics_service.get_average_experience,
        "has_plot": False,
        "title": "Средний опыт сотрудников",
        "description": "Вычисляет средний стаж работы сотрудников в компании в том числе с фильтрами и группировками, например по возрасту, полу и т.д"
    },
    "average-age": {
        "func": analytics_service.get_average_fullyears,
        "has_plot": False,
        "title": "Средний возраст сотрудников",
        "description": "Вычисляет средний возраст всех сотрудников"
    },
    "count-by-sex": {
        "func": analytics_service.get_count_by_sex,
        "title": "Количество сотрудников по полу",
        "has_plot": True,
        "flat_result": True,
        "type_chart": 'pie',
        "description": "Считает количество мужчин и женщин в компании"
    },
    "employees-by-region": {
        "func": analytics_service.get_employees_by_region,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Количество сотрудников по регионам",
        "big": True,
        "description": "Считает сотрудников в разных регионах компании"
    },
    "average-tenure-until-fire": {
        "func": analytics_service.get_average_tenure_until_fire,
        "has_plot": False,
        "title": "Средний срок работы до увольнения",
        "description": "Вычисляет средний период работы сотрудников до их увольнения"
    },
    "average-fte": {
        "func": analytics_service.get_average_fte,
        "has_plot": True,
        "title": "Средний FTE сотрудников",
        "description": "Считает средний FTE сотрудников, поддерживает фильтры и группировки по любым полям (например service, sex, region, department_3 и т.д.)"
    },

    "fired-count": {
        "func": analytics_service.get_fired_count,
        "has_plot": False,
        "title": "Общее количество увольнений",
        "description": "Подсчитывает общее количество увольнений сотрудниковподдерживает фильтры и группировки по любым полям (например service, sex, region, department_3 и т.д.)"
    },
    "hire-count": {
        "func": analytics_service.get_hire_count,
        "has_plot": False,
        "title": "Общее количество найма",
        "description": "Подсчитывает общее количество новых сотрудников, принятых в компанию"
    },
    "count-by-work-form": {
        "func": analytics_service.get_count_by_work_form,
        "has_plot": True,
        "type_chart": 'pie',
        "flat_result": True,
        "title": "Количество сотрудников по форме работы офис/удаленка",
        "description": "Считает, сколько сотрудников работают в офисе и сколько удалённо"
    },
    "fte-sum": {
        "func": analytics_service.get_fte_sum,
        "has_plot": False,
        "title": "Сумма ставок FTE",
        "description": "Вычисляет суммарное количество ставок FTE всех сотрудников"
    },
    "fte-mean": {
        "func": analytics_service.get_fte_mean,
        "has_plot": False,
        "title": "Средний FTE",
        "description": "Вычисляет среднюю ставку FTE по всем сотрудникам"
    },
    "turnover": {
        "func": analytics_service.get_turnover,
        "has_plot": True,
        "title": "Текучесть кадров",
        "big": True,
        "description": "Текучесть кадров (%), с учётом фильтров, периода и группировки"
    },

    "hires-and-fires-share": {
        "func": analytics_service.get_hires_and_fires_share,
        "has_plot": True,
        "type_chart": 'doughnut',
        "title": "Доля новых наймов и увольнений",
        "description": "Показывает долю новых сотрудников и увольнений с учётом фильтров, периода и группировки"
    },
    "work-form-distribution": {
        "func": analytics_service.get_work_form_distribution,
        "has_plot": True,
        "type_chart": 'pie',
        "flat_result": True,
        "title": "Доля сотрудников по формам работы - офис/удаленка",
        "description": "Показывает процентное соотношение сотрудников в офисе и удалённо"
    },
    "employee-count": {
        "func": analytics_service.get_employee_count,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Количество сотрудников",
        "big": True,
        "description": "Количество сотрудников с учётом фильтров, периода и группировки (по сервисам, департаментам, отделам, месяцам, полу и тд)"
    },
    "total-employees": {
        "func": analytics_service.get_total_employees,
        "has_plot": False,
        "title": "Общее количество сотрудников",
        "description": "Общее количество сотрудников"
    },
    "hires-to-cover-turnover": {
        "func": analytics_service.get_hires_to_cover_turnover,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Покрытие оттока",
        "description": "Показывает сколько сотрудников нужно нанимать каждый месяц, чтобы покрыть отток"
    },
    "high-turnover-departments": {
        "func": analytics_service.get_high_turnover_departments,
        "has_plot": True,
        "type_chart": 'bar',
        "big": True,
        "title": "Отделы с самой высокой текучестью кадров",
        "description": "Показывает  отделы с самой высокой текучестью кадров"
    },
    "turnover-trend": {
        "func": analytics_service.get_turnover_trend,
        "has_plot": True,
        "type_chart": 'line',
        "title": "Динамика текучести кадров",
        "description": "Показывает динамику текучести кадров"
    },
    "at-risk-departments": {
        "func": analytics_service.get_at_risk_departments,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Отделы в зоне риска",
        "description": "Находит отделы в зоне риска: высокая текучесть + низкий FTE + низкий опыт"
    },
    "most-stable-departments": {
        "func": analytics_service.get_most_stable_departments,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Отделы с низкой текучестью",
        "description": "Находит отделы с низкой текучестью + высоким средним стажем"
    },
    "firing-trends-by-age": {
        "func": analytics_service.get_firing_trends_by_age,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Тренд увольнений по возрастным группам",
        "description": "Показывает как меняется увольнения по возрастным группам по месяцам"
    },
    "hiring-trends-by-department": {
        "func": analytics_service.get_hiring_trends_by_department,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Тренд найма по отделам",
        "description": "Показывает как меняется найм по отделам"
    },
}
