from django.db import migrations


def create_canonical_exercises(apps, schema_editor):
    Exercise = apps.get_model('physiotherapy', 'Exercise')

    # remove any existing exercises
    Exercise.objects.all().delete()

    canonical = [
        # Back pain level 1-3
        {
            'name': 'Back - Full Range (Level 1)',
            'exercise_type': 'back',
            'pain_level': 1,
            'description': 'Full-range back extension for prevention and mobility.',
            'duration_minutes': 10,
            'instructions': 'Stand upright, pull shoulders back, squeeze shoulder blades. Hold 20-30 seconds and repeat 8-10 times.',
            'image_url': 'images/back_pain_level1.gif',
            'video_url': '',
            'is_active': True,
        },
        {
            'name': 'Back - Moderate Range (Level 2)',
            'exercise_type': 'back',
            'pain_level': 2,
            'description': 'Moderate back extension with controlled range for intermediate pain.',
            'duration_minutes': 8,
            'instructions': 'Pull shoulders back halfway, hold 10-15 seconds. Repeat 5-8 times, 2-3 sets daily.',
            'image_url': 'images/back_pain_level2.gif',
            'video_url': '',
            'is_active': True,
        },
        {
            'name': 'Back - Gentle Movement (Level 3)',
            'exercise_type': 'back',
            'pain_level': 3,
            'description': 'Very gentle back movement focused on comfort and recovery.',
            'duration_minutes': 5,
            'instructions': 'Very small, gentle movements. Hold for 5-8 seconds. 3-5 repetitions, 2 times daily.',
            'image_url': 'images/back_pain_level3.gif',
            'video_url': '',
            'is_active': True,
        },

        # Elbow pain level 1-3
        {
            'name': 'Elbow - Full Range (Level 1)',
            'exercise_type': 'elbow',
            'pain_level': 1,
            'description': 'Full-range elbow flexion and extension for prevention and mobility.',
            'duration_minutes': 10,
            'instructions': 'Bend and straighten the elbow slowly. Hold end positions briefly. Repeat 10-15 times.',
            'image_url': 'images/elbow_pain_level1.gif',
            'video_url': '',
            'is_active': True,
        },
        {
            'name': 'Elbow - Moderate Range (Level 2)',
            'exercise_type': 'elbow',
            'pain_level': 2,
            'description': 'Moderate elbow movements for intermediate pain control.',
            'duration_minutes': 8,
            'instructions': 'Perform controlled flexion to a moderate range. Hold 5-10 seconds. Repeat 8-10 times.',
            'image_url': 'images/elbow_pain_level2.gif',
            'video_url': '',
            'is_active': True,
        },
        {
            'name': 'Elbow - Gentle Movement (Level 3)',
            'exercise_type': 'elbow',
            'pain_level': 3,
            'description': 'Minimal, gentle elbow movement for recovery.',
            'duration_minutes': 5,
            'instructions': 'Very gentle flexion/extension. 3-5 repetitions, 2 times daily. Stop if pain increases.',
            'image_url': 'images/elbow_pain_level3.gif',
            'video_url': '',
            'is_active': True,
        },

        # Neck pain level 1-3
        {
            'name': 'Neck - Full Range (Level 1)',
            'exercise_type': 'neck',
            'pain_level': 1,
            'description': 'Full-range neck rotations and tilts to maintain mobility.',
            'duration_minutes': 10,
            'instructions': 'Rotate head slowly to each side and perform forward/backward tilts. Hold 5-10 seconds. Repeat 8 times.',
            'image_url': 'images/neck_pain_level1.gif',
            'video_url': '',
            'is_active': True,
        },
        {
            'name': 'Neck - Moderate Range (Level 2)',
            'exercise_type': 'neck',
            'pain_level': 2,
            'description': 'Moderate neck movements with reduced range to avoid strain.',
            'duration_minutes': 8,
            'instructions': 'Small rotations (12-18°). Brief forward/backward tilts. Hold 3-5 seconds. Repeat 5-8 times.',
            'image_url': 'images/neck_pain_level2.gif',
            'video_url': '',
            'is_active': True,
        },
        {
            'name': 'Neck - Gentle Movement (Level 3)',
            'exercise_type': 'neck',
            'pain_level': 3,
            'description': 'Very gentle neck movement focused on comfort and healing.',
            'duration_minutes': 5,
            'instructions': 'Minimal head movement only. 2-3 repetitions, 2 times daily. Stop if pain increases.',
            'image_url': 'images/neck_pain_level3.gif',
            'video_url': '',
            'is_active': True,
        },
    ]

    for data in canonical:
        Exercise.objects.create(**data)


def delete_canonical_exercises(apps, schema_editor):
    Exercise = apps.get_model('physiotherapy', 'Exercise')
    names = [
        'Back - Full Range (Level 1)',
        'Back - Moderate Range (Level 2)',
        'Back - Gentle Movement (Level 3)',
        'Elbow - Full Range (Level 1)',
        'Elbow - Moderate Range (Level 2)',
        'Elbow - Gentle Movement (Level 3)',
        'Neck - Full Range (Level 1)',
        'Neck - Moderate Range (Level 2)',
        'Neck - Gentle Movement (Level 3)',
    ]
    Exercise.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('physiotherapy', '0011_alter_exercise_options_remove_exercise_difficulty'),
    ]

    operations = [
        migrations.RunPython(create_canonical_exercises, delete_canonical_exercises),
    ]
