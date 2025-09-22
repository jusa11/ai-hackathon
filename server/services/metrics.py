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
        "description": "Вычисляет средний стаж работы сотрудников в компании"
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
        "type_chart": 'pie',
        "description": "Считает количество мужчин и женщин в компании"
    },

    "count-by-department-level": {
        "func": analytics_service.get_count_by_department_level,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Количество сотрудников в департаменте",
        "description": "Показывает распределение сотрудников по уровням департамента"
    },
    "get-employees-by-region": {
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
    "average-experience-by-department": {
        "func": analytics_service.get_average_experience_by_department,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Средний опыт сотрудников в департаменте",
        "description": "Вычисляет средний стаж работы сотрудников по департаментам"
    },
    "average-fte-by-department": {
        "func": analytics_service.get_average_fte_by_department,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Средний FTE в департаменте",
        "description": "Считает среднюю ставку FTE сотрудников по департаментам"
    },
    "average-experience-by-region": {
        "func": analytics_service.get_average_experience_by_region,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Средний опыт работников по регионам",
        "description": "Вычисляет средний стаж работы сотрудников по регионам"
    },
    "fired-count": {
        "func": analytics_service.get_fired_count,
        "has_plot": False,
        "title": "Общее количество увольнений",
        "description": "Подсчитывает общее количество увольнений сотрудников"
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
    "turnover-rate-by-month": {
        "func": analytics_service.get_turnover_rate_by_month,
        "has_plot": False,
        "type": 'bar',
        "title": "Текучесть кадров за выбранные месяцы",
        "description": "Показывает текучесть сотрудников по месяцам"
    },
    "turnover-rate-by-department": {
        "func": analytics_service.get_turnover_rate_by_department,
        "has_plot": False,
        "title": "Текучесть в департаменте",
        "description": "Вычисляет текучесть сотрудников в каждом департаменте"
    },
    "hires-and-fires-share-by-department": {
        "func": analytics_service.get_hires_and_fires_share_by_department,
        "has_plot": True,
        "type_chart": 'doughnut',
        "title": "Доля новых наймов и увольнений в департаменте",
        "description": "Показывает долю новых сотрудников и увольнений по департаментам"
    },
    "turnover-rate-all-regions": {
        "func": analytics_service.get_turnover_rate_all_regions,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Текучесть по всем регионам",
        "description": "Сравнивает текучесть сотрудников по регионам"
    },
    "work-form-distribution": {
        "func": analytics_service.get_work_form_distribution,
        "has_plot": True,
        "type_chart": 'pie',
        "title": "Доля сотрудников по формам работы - офис/удаленка",
        "description": "Показывает процентное соотношение сотрудников в офисе и удалённо"
    },
    "average-fte-by-work-form": {
        "func": analytics_service.get_average_fte_by_work_form,
        "has_plot": True,
        "type_chart": 'pie',
        "title": "Средняя ставка FTE по формам работы - офис/удаленка",
        "description": "Вычисляет среднюю ставку FTE для офисных и удалённых сотрудников"
    },
    "turnover-rate-by-age-category": {
        "func": analytics_service.get_turnover_rate_by_age_category,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Текучесть по возрастным категориям",
        "description": "Показывает текучесть по разным возрастным категориям сотрудников"
    },
    "turnover-rate-by-experience-category": {
        "func": analytics_service.get_turnover_rate_by_experience_category,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Текучесть по категориям опыта",
        "description": "Показывает текучесть сотрудников по категориям опыта"
    },
    "average-experience-by-group": {
        "func": analytics_service.get_average_experience_by_group,
        "has_plot": False,
        "title": "Средний стаж по сервису или отделу",
        "description": "Вычисляет средний стаж по отдельным сервисам или отделам"
    },
    "turnover-rate-by-service": {
        "func": analytics_service.get_turnover_rate_by_service,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Текучесть по сервисам",
        "description": "Показывает текучесть сотрудников по сервисам компании"
    },
    "turnover-rate-by-work-form": {
        "func": analytics_service.get_turnover_rate_by_work_form,
        "has_plot": True,
        "type_chart": 'pie',
        "title": "Текучесть по форме работы - офис/удаленка",
        "description": "Сравнивает текучесть между офисными и удалёнными сотрудниками"
    },
    "fired-count-by-region": {
        "func": analytics_service.get_fired_count_by_region,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Количество увольнений по регионам",
        "description": "Считает количество увольнений сотрудников по регионам"
    },
    "employee-count-by-service": {
        "func": analytics_service.get_employee_count_by_service,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Количество сотрудников по сервисам",
        "description": "Считает количество сотрудников в каждом сервисе"
    },
    "average-fte-by-service": {
        "func": analytics_service.get_average_fte_by_service,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Средний FTE по сервисам",
        "description": "Вычисляет средний FTE сотрудников по каждому сервису"
    },
    "average-experience-by-region": {
        "func": analytics_service.get_average_experience_by_region,
        "has_plot": True,
        "type_chart": 'bar',
        "title": "Средний стаж по регионам",
        "description": "Вычисляет средний стаж сотрудников в разных регионах"
    }
}
