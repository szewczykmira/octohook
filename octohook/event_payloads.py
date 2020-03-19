from abc import ABC

from octohook.common import Repository, Organization, User, Comment, CheckRun, CheckSuite, Installation, DeployKey, \
    Deployment, DeploymentStatus, Page, ShortRepository, Issue, Label, MarketplacePurcahase, Team, Hook, Milestone, \
    Membership, Package, PageBuild, ProjectCard, ProjectColumn, Project, PullRequest, Review, Release, \
    VulnerabilityAlert, SecurityAdvisory, Sponsorship, Branch, StatusCommit, RawDict, \
    ContentReference, Commit, CommitUser, optional


class WebhookEvent(ABC):
    def __init__(self, payload: dict):
        self.action = payload.get('action')
        self.sender = User(payload.get('sender'))

        # Not present in GitHubAppAuthorizationEvent, InstallationEvent, SponsorshipEvent
        try:
            self.repository = Repository(payload.get('repository'))
        except AttributeError:
            pass

        # Only present in some events
        try:
            self.organization = Organization(payload.get('organization'))
        except AttributeError:
            pass


class CheckRunEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#checkrunevent
    """

    def __init__(self, payload: dict):
        super().__init__(payload)
        self.check_run = CheckRun(payload.get('check_run'))


class CheckSuiteEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#checksuiteevent
    """

    def __init__(self, payload: dict):
        super().__init__(payload)
        self.check_suite = CheckSuite(payload.get('check_suite'))


class CommitCommentEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#commitcommentevent
    """

    def __init__(self, payload: dict):
        super().__init__(payload)
        self.comment = Comment(payload.get('comment'))


class ContentReferenceEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#contentreferenceevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.content_reference = ContentReference(payload.get('content_reference'))
        self.installation = Installation(payload.get('installation'))


class CreateEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#createevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.ref = payload.get('ref')
        self.ref_type = payload.get('ref_type')
        self.master_branch = payload.get('master_branch')
        self.description = payload.get('description')
        self.pusher_type = payload.get('pusher_type')


class DeleteEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#deleteevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.ref = payload.get('ref')
        self.ref_type = payload.get('ref_type')
        self.pusher_type = payload.get('pusher_type')


class DeployKeyEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#deploykeyevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.key = DeployKey(payload.get('key'))


class DeploymentEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#deploymentevent
    """

    def __init__(self, payload):
        super().__init__(payload)

        self.deployment = Deployment(payload.get('deployment'))


class DeploymentStatusEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#deploymentstatusevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.deployment_status = DeploymentStatus(payload.get('deployment_status'))
        self.deployment = Deployment(payload.get('deployment'))


class ForkEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#forkevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.forkee = Repository(payload.get('forkee'))


class GitHubAppAuthorizationEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#forkapplyevent
    """

    def __init__(self, payload):
        super().__init__(payload)


class GollumEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#gollumevent
    """

    def __init__(self, payload):
        super().__init__(payload)

        self.pages = [Page(page) for page in payload.get('pages')]


class InstallationEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#installationevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.installation = Installation(payload.get('installation'))

        self.repositories = [ShortRepository(repo) for repo in payload.get('repositories')]


class InstallationRepositoriesEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#installationrepositoriesevent
    """

    def __init__(self, payload):
        super().__init__(payload)

        self.installation = Installation(payload.get('installation'))
        self.repository_selection = payload.get('repository_selection')
        self.repositories_added = [ShortRepository(repo) for repo in payload.get('repositories_added')]
        self.repositories_removed = [ShortRepository(repo) for repo in payload.get('repositories_removed')]


class IssueCommentEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#issuecommentevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.issue = Issue(payload.get('issue'))
        self.comment = Comment(payload.get('comment'))
        self.changes = optional(payload, 'changes', RawDict)


class IssuesEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#issuesevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.issue = Issue(payload.get('issue'))
        self.changes = optional(payload, 'changes', RawDict)
        self.label = optional(payload, 'label', Label)
        self.assignee = optional(payload, 'assignee', User)
        self.milestone = optional(payload, 'milestone', Milestone)


class LabelEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#labelevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.label = Label(payload.get('label'))
        self.changes = optional(payload, 'changes', RawDict)


class MarketplacePurchaseEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#marketplacepurchaseevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.effective_date = payload.get('effective_date')
        self.marketplace_purchase = MarketplacePurcahase(payload.get('marketplace_purchase'))


class MemberEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#memberevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.member = User(payload.get('member'))


class MembershipEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#membershipevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.scope = payload.get('scope')
        self.member = User(payload.get('member'))
        self.team = Team(payload.get('team'))


class MetaEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#metaevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.hook_id = payload.get('hook_id')
        self.hook = Hook(payload.get('hook'))


class MilestoneEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#milestoneevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.milestone = Milestone(payload.get('milestone'))
        self.changes = optional(payload, 'changes', RawDict)


class OrganizationEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#organizationevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.invitation = payload.get('invitation')  # TODO: What does this look like?
        self.membership = Membership(payload.get('membership'))


class OrgBlockEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#orgblockevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.blocked_user = User(payload.get('blocked_user'))


class PackageEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#packageevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.package = Package(payload.get('package'))


class PageBuildEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#pagebuildevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.id = payload.get('id')
        self.build = PageBuild(payload.get('build'))


class ProjectCardEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#projectcardevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.project_card = ProjectCard(payload.get('project_card'))
        self.changes = optional(payload, 'changes', RawDict)


class ProjectColumnEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#projectcolumnevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.project_column = ProjectColumn(payload.get('project_column'))
        self.changes = optional(payload, 'changes', RawDict)


class ProjectEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#projectevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.project = Project(payload.get('project'))


class PublicEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#publicevent
    """

    def __init__(self, payload):
        super().__init__(payload)


class PullRequestEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#pullrequestevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.number = payload.get('number')
        self.pull_request = PullRequest(payload.get('pull_request'))
        self.assignee = optional(payload, 'assignee', User)
        self.label = optional(payload, 'label', Label)
        self.changes = optional(payload, 'changes', RawDict)
        self.before = payload.get('before')
        self.after = payload.get('after')
        self.requested_reviewer = optional(payload, 'requested_reviewer', User)


class PullRequestReviewEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#pullrequestreviewevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.review = Review(payload.get('review'))
        self.pull_request = PullRequest(payload.get('pull_request'))
        self.changes = RawDict(payload.get('pull_request'))


class PullRequestReviewCommentEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#pullrequestreviewcommentevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.comment = Comment(payload.get('comment'))
        self.pull_request = PullRequest(payload.get('pull_request'))
        self.changes = optional(payload, 'changes', RawDict)


class PushEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#pushevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.ref = payload.get('ref')
        self.before = payload.get('before')
        self.after = payload.get('after')
        self.created = payload.get('created')
        self.deleted = payload.get('deleted')
        self.forced = payload.get('forced')
        self.base_ref = payload.get('base_ref')
        self.compare = payload.get('compare')
        self.commits = [Commit(commit) for commit in payload.get('commits')]
        self.head_commit = optional(payload, 'head_commit', Commit)
        self.pusher = CommitUser(payload.get('pusher'))


class ReleaseEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#releaseevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.release = Release(payload.get('release'))
        self.changes = RawDict(payload.get('release'))


class RepositoryDispatchEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#repositorydispatchevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.branch = payload.get('branch')
        self.client_payload = RawDict(payload.get('client_payload'))
        self.installation = Installation(payload.get('installation'))


class RepositoryEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#repositoryevent
    """

    def __init__(self, payload):
        super().__init__(payload)


class RepositoryImportEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#repositoryimportevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.status = payload.get('status')


class RepositoryVulnerabilityAlertEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#repositoryvulnerabilityalertevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.alert = VulnerabilityAlert(payload.get('alert'))


class SecurityAdvisoryEvent:
    """
    https://developer.github.com/v3/activity/events/types/#securityadvisoryevent
    """

    def __init__(self, payload):
        self.action = payload.get('action')
        self.security_advisory = SecurityAdvisory(payload.get('security_advisory'))


class SponsorshipEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#sponsorshipevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.sponsorship = Sponsorship(payload.get('sponsorship'))
        try:
            self.changes = optional(payload, 'changes', RawDict)
            self.effective_date = payload.get('effective_date', None)
        except KeyError:
            pass


class StarEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#starevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.starred_at = payload.get('starred_at')


class StatusEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#statusevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.id = payload.get('id')
        self.sha = payload.get('sha')
        self.name = payload.get('name')
        self.target_url = payload.get('target_url')
        self.context = payload.get('context')
        self.description = payload.get('description')
        self.state = payload.get('state')
        self.commit = StatusCommit(payload.get('commit'))
        self.branches = [Branch(branch) for branch in payload.get('branches')]
        self.created_at = payload.get('created_at')
        self.updated_at = payload.get('updated_at')


class TeamEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#teamevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.team = Team(payload.get('team'))


class TeamAddEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#teamaddevent
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.team = Team(payload.get('team'))


class WatchEvent(WebhookEvent):
    """
    https://developer.github.com/v3/activity/events/types/#watchevent
    """

    def __init__(self, payload):
        super().__init__(payload)