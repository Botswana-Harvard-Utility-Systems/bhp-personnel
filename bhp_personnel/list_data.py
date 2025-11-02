from edc_list_data import PreloadData


list_data = {
    'bhp_personnel.studies': [
        ('potlako', 'Potlako'),
        ('ambition', 'Ambition'),
        ('cancer', 'Cancer'),
        ('flourish', 'Flourish'),
        ('agrdt', 'AGRDT'),
    ],
    'bhp_personnel.skills': [
        ('strategic_orientation', 'Strategic Orientation'),
        ('results_focus', 'Results Focus'),
        ('leadership_and_motivation', 'Leadership and Motivation'),
        ('innovation_and_creativity', 'Innovation and Creativity'),
        ('planning_skills', 'Planning'),
        ('interpersonal_skills', 'Interpersonal'),
        ('communication_skills', 'Communication'),
        ('knowledge_and_productivity', 'Knowledge and Productivity'),
        ('quality_of_work', 'Quality of work')
    ]
}

preload_data = PreloadData(
    list_data=list_data)
