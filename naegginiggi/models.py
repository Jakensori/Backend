# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Campaign(models.Model):
    campaign_id = models.IntegerField(primary_key=True)
    rdonaboxno = models.CharField(db_column='rdonaBoxNo', max_length=45, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    hlogname = models.CharField(db_column='hlogName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    startymd = models.DateTimeField(db_column='startYmd', blank=True, null=True)  # Field name made lowercase.
    endymd = models.DateTimeField(db_column='endYmd', blank=True, null=True)  # Field name made lowercase.
    currentamount = models.IntegerField(db_column='currentAmount', blank=True, null=True)  # Field name made lowercase.
    donationcount = models.IntegerField(db_column='donationCount', blank=True, null=True)  # Field name made lowercase.
    goalamount = models.IntegerField(db_column='goalAmount', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Campaign'


class DonationPoint(models.Model):
    donation_point_id = models.IntegerField(primary_key=True)
    donation_point_userid = models.ForeignKey('User', models.DO_NOTHING, db_column='donation_point_userid')
    point = models.IntegerField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Donation_Point'


class Message(models.Model):
    message_campaignid = models.ForeignKey(Campaign, models.DO_NOTHING, db_column='message_campaignid')
    message_userid = models.ForeignKey('User', models.DO_NOTHING, db_column='message_userid')
    message = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Message'


class Record(models.Model):
    record_id = models.IntegerField(primary_key=True)
    record_user_record = models.ForeignKey('UserRecord', models.DO_NOTHING)
    when = models.CharField(max_length=30, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    memo = models.TextField(blank=True, null=True)
    settlement = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Record'


class Review(models.Model):
    review_id = models.IntegerField(primary_key=True)
    campaign = models.ForeignKey(Campaign, models.DO_NOTHING)
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=10000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Review'


class User(models.Model):
    user = models.OneToOneField('AuthUser', models.DO_NOTHING, primary_key=True)
    username = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User'


class UserCampaign(models.Model):
    user_campaign_userid = models.ForeignKey(User, models.DO_NOTHING, db_column='user_campaign_userid')
    user_campaignid = models.ForeignKey(Campaign, models.DO_NOTHING, db_column='user_campaignid')

    class Meta:
        managed = False
        db_table = 'User_Campaign'


class UserCustom(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    month_budget = models.IntegerField(blank=True, null=True)
    donation_temperature = models.FloatField(blank=True, null=True)
    total_donation = models.IntegerField(blank=True, null=True)
    donation_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User_Custom'


class UserRecord(models.Model):
    userrecord_userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userrecord_userid')
    userrecord_id = models.IntegerField(primary_key=True)
    day_budget = models.IntegerField(blank=True, null=True)
    today_date = models.DateTimeField(blank=True, null=True)
    consumption = models.IntegerField(blank=True, null=True)
    donation = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User_Record'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CampaignCampaign(models.Model):
    id = models.BigAutoField(primary_key=True)
    rdonaboxno = models.CharField(db_column='rdonaBoxNo', max_length=100)  # Field name made lowercase.
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    summary = models.TextField()
    hlogname = models.CharField(db_column='hlogName', max_length=50)  # Field name made lowercase.
    startymd = models.DateTimeField(db_column='startYmd')  # Field name made lowercase.
    endymd = models.DateTimeField(db_column='endYmd')  # Field name made lowercase.
    currentamount = models.IntegerField(db_column='currentAmount')  # Field name made lowercase.
    donationcount = models.IntegerField(db_column='donationCount')  # Field name made lowercase.
    goalamount = models.IntegerField(db_column='goalAmount')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'campaign_campaign'


class CampaignMessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    message = models.TextField()
    campaign = models.ForeignKey(CampaignCampaign, models.DO_NOTHING)
    user = models.ForeignKey('UserUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'campaign_message'


class CampaignReview(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    campaign = models.ForeignKey(CampaignCampaign, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'campaign_review'


class CampaignUserCampaign(models.Model):
    id = models.BigAutoField(primary_key=True)
    campaign = models.ForeignKey(CampaignCampaign, models.DO_NOTHING)
    user = models.ForeignKey('UserUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'campaign_user_campaign'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class KnoxAuthtoken(models.Model):
    digest = models.CharField(primary_key=True, max_length=128)
    created = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    expiry = models.DateTimeField(blank=True, null=True)
    token_key = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'knox_authtoken'


class UserUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_user'
