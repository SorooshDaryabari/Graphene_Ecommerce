from accounts.models import (
    Ticket,
    TicketAnswer,
)
from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType
from graphql_auth import mutations
from graphql_auth.schema import MeQuery, UserQuery
import graphene
import graphql_jwt
from graphene_django.rest_framework.mutation import SerializerMutation
from accounts.serializers import TicketSerializer


class TicketObjectType(DjangoObjectType):
    class Meta:
        model = Ticket
        fields = (
            "title",
            "user_text",
            "created_at",
        )


class TicketAnswerObjectType(DjangoObjectType):
    class Meta:
        model = TicketAnswer
        fields = (
            "ticket",
            "answer",
        )


class AccountObjectType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = (
            "first_name", "last_name", "username", "email",
            "is_supporter", "is_staff", "phone_number",
            "state", "city", "address", "zip_code",
        )


class TicketMutation(SerializerMutation):
    class Meta:
        serializer_class = TicketSerializer
        model_operations = ("create", "update")
        lookup_field = "id"


class Query(UserQuery, MeQuery, graphene.ObjectType):
    all_tickets = graphene.List(TicketObjectType)
    ticket = graphene.Field(TicketObjectType, id=graphene.Int())

    ticket_answer = graphene.Field(TicketAnswerObjectType, id=graphene.Int())

    def resolve_all_tickets(root, info):
        return Ticket.objects.filter(owner=info.context.user).order_by("-id")

    def resolve_ticket(self, info, id):
        try:
            if info.context.user.is_authenticated:
                ticket = Ticket.objects.get(id=id)
                if (
                        ticket.owner == info.context.user and
                        info.context.user.is_active
                ):
                    return ticket

            else:
                return {
                    "404NotFound": "Object not found",
                }

        except Ticket.DoesNotExist:
            return {
                "404NotFound": "Object not found",
            }

    def resolve_ticket_answer(self, info, id):
        try:
            if info.context.user.is_authenticated:
                ticket_answer = TicketAnswer.objects.get(ticket_id=id)
                if (
                        info.context.user.is_active and
                        info.context.user == ticket_answer.ticket.owner
                ):
                    return ticket_answer

                else:
                    return {
                        "404NotFound": "Object not found"
                    }

        except TicketAnswer.DoesNotExist:
            return {
                "404NotFound": "Object not found"
            }


class Mutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()

    # django-graphql-jwt inheritances
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = mutations.RevokeToken.Field()

    # Create and update ticket
    create_and_update_ticket = TicketMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
