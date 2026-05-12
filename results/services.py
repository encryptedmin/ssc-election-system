from django.db.models import Count
from django.utils import timezone

from accounts.models import User
from candidates.models import Candidate, Position
from voting.models import Vote


def get_election_results(election):
    registered_voters = User.objects.filter(
        role='VOTER',
        is_approved=True
    )
    votes = Vote.objects.filter(
        election=election
    )
    positions = Position.objects.filter(
        election=election
    ).order_by('order', 'name')
    candidates = Candidate.objects.filter(
        election=election
    )

    registered_count = registered_voters.count()
    voted_count = votes.values('voter_id').distinct().count()

    return {
        'election': _election_data(election),
        'summary': _summary_data(
            registered_count=registered_count,
            voted_count=voted_count,
            vote_count=votes.count(),
            position_count=positions.count(),
            candidate_count=candidates.count(),
        ),
        'positions': _position_results(
            positions=positions,
            candidates=candidates,
            votes=votes,
        ),
        'department_participation': _department_participation(
            registered_voters=registered_voters,
            votes=votes,
        ),
        'generated_at': timezone.localtime().strftime('%b %d, %Y %I:%M:%S %p'),
    }


def _election_data(election):
    return {
        'id': election.id,
        'title': election.title,
        'description': election.description,
        'is_active': election.is_active,
        'is_open': election.is_open,
        'is_concluded': election.is_concluded,
        'status_label': election.status_label,
        'start_time': election.start_time.strftime('%b %d, %Y %I:%M %p'),
        'end_time': election.end_time.strftime('%b %d, %Y %I:%M %p'),
    }


def _summary_data(
    registered_count,
    voted_count,
    vote_count,
    position_count,
    candidate_count
):
    return {
        'registered_voters': registered_count,
        'voted_voters': voted_count,
        'not_voted': max(registered_count - voted_count, 0),
        'turnout_percentage': _percentage(voted_count, registered_count),
        'total_votes': vote_count,
        'total_positions': position_count,
        'total_candidates': candidate_count,
    }


def _position_results(positions, candidates, votes):
    results = []

    for position in positions:
        candidate_results = _candidate_results(
            position=position,
            candidates=candidates.filter(
                position=position
            ).order_by('fullname'),
            votes=votes,
        )

        results.append({
            'id': position.id,
            'name': position.name,
            'max_votes': position.max_votes,
            'total_votes': sum(
                candidate['votes'] for candidate in candidate_results
            ),
            'candidates': candidate_results,
        })

    return results


def _candidate_results(position, candidates, votes):
    results = []

    for candidate in candidates:
        vote_count = votes.filter(
            position=position,
            candidate=candidate
        ).count()

        results.append({
            'id': candidate.id,
            'name': candidate.fullname,
            'photo_url': candidate.photo.url if candidate.photo else '',
            'platform': candidate.platform,
            'votes': vote_count,
            'percentage': 0,
            'is_winner': False,
        })

    total_votes = sum(
        candidate['votes'] for candidate in results
    )
    top_votes = max(
        [candidate['votes'] for candidate in results],
        default=0
    )

    for candidate in results:
        candidate['percentage'] = _percentage(
            candidate['votes'],
            total_votes
        )
        candidate['is_winner'] = top_votes > 0 and candidate['votes'] == top_votes

    return sorted(
        results,
        key=lambda candidate: (
            -candidate['votes'],
            candidate['name'].lower()
        )
    )


def _department_participation(registered_voters, votes):
    registered_by_department = {
        _department_name(row['department']): row['total']
        for row in registered_voters.values('department').annotate(
            total=Count('id')
        )
    }

    voted_by_department = {
        _department_name(row['voter__department']): row['total']
        for row in votes.filter(
            voter__role='VOTER',
            voter__is_approved=True
        ).values('voter__department').annotate(
            total=Count('voter_id', distinct=True)
        )
    }

    departments = sorted(
        set(registered_by_department) | set(voted_by_department)
    )

    return [
        {
            'department': department,
            'registered': registered_by_department.get(department, 0),
            'voted': voted_by_department.get(department, 0),
            'percentage': _percentage(
                voted_by_department.get(department, 0),
                registered_by_department.get(department, 0)
            ),
        }
        for department in departments
    ]


def _department_name(department):
    if department and department.strip():
        return department.strip()

    return 'Unassigned'


def _percentage(part, whole):
    if not whole:
        return 0

    return round((part / whole) * 100, 1)
