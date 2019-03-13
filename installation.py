from flask import Flask, request, redirect, url_for
from flask_restful import Api, Resource, reqparse
import os
import io
from werkzeug.utils import secure_filename
import csv
import boto3

table = dynamodb.create_table(
    TableName='openpositions',
    KeySchema=[
        {
            'AttributeName': 'serialno',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'serialno',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'Code',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'Position',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'Description',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'Mandatory Skills',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'Soft Skills',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'Experience',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'Level 1',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'Level 2',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'Status',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'createdat',
            'AttributeType': 'S'
        }
    ],
    LocalSecondaryIndexes=[
        {
            'IndexName': 'createddatetimeIndex',
            KeySchema=[
                {
                    'AttributeName': 'serialno',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'createdat',
                    'KeyType': 'RANGE'
                }
            ],
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

table.meta.client.get_waiter('table_exists').wait(TableName='openpositions')

# Print out some data about the table.
print(table.item_count)