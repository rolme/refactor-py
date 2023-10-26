from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
)
from constructs import Construct
# import python_minifier as minifier

class RefactorStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #######################################################################
        # DynamoDB

        # Create the DynamoDB table
        table = dynamodb.Table(
            self, 'RefactorTable',
            partition_key=dynamodb.Attribute(
                name='hashKey',
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name='rangeKey',
                type=dynamodb.AttributeType.STRING
            ),
            table_name='REFACTOR_TABLE',
            removal_policy=RemovalPolicy.DESTROY  # Only for dev/test environments
        )

        # Add the itemTypeIdIndex (itemType, id)
        table.add_global_secondary_index(
            index_name='itemTypeIdIndex',
            partition_key=dynamodb.Attribute(
                name='itemType',
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name='id',
                type=dynamodb.AttributeType.STRING
            )
        )

        #######################################################################
        # Lambda

        user_lambda = _lambda.Function(
            self, 'UserLambda',
            code=_lambda.Code.from_asset('./lambdas'),
            environment={
                'TABLE_NAME': 'REFACTOR_TABLE'
            },
            handler='user.handler',
            runtime=_lambda.Runtime.PYTHON_3_11,
            timeout=Duration.seconds(900),
        )

        # Grant the Lambda function permissions full access to the DynamoDB table
        table.grant_read_write_data(user_lambda)
        