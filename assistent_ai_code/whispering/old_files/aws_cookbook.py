import boto3
import time
import os
import sys
import paramiko
import getpass
import socket
import select
import threading
import subprocess
# write a function that will start a new VPC instance in AWS and then connect to it using AWS Lightsail
def start_new_instance():
    """
    This function starts a new VPC instance in AWS and then connects to it using AWS Lightsail
    """
    # create a new Lightsail client


    # create a new instance
    response = client.create_instances(
        instanceNames=[
            'whispering',
        ],
        availabilityZone='us-west-2a',
        blueprintId='amazon_linux_2',
        bundleId='nano_2_0',
        keyPairName='whispering',
        userData='''#!/bin/bash
        sudo apt update
        sudo apt install python3-pip -y
        sudo apt install python3-venv -y
        sudo apt install git -y
        git clone
        cd whispering
        python3 -m venv venv
        source venv/bin/activate
        pip3 install -r requirements.txt
        python3 whispering.py
        ''',
    )
#     print(response)   
    # wait for the instance to start
    time.sleep(60)
    # get the public IP address of the instance
    response = client.get_instance(
        instanceName='whispering',
    )
    # print the public IP address of the instance
    print(response['instance']['publicIpAddress'])
    # create a new SSH client
    ssh = paramiko.SSHClient()
    # add the host key
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # connect to the instance
    ssh.connect(hostname=response['instance']['publicIpAddress'], username='ubuntu', key_filename='/Users/canyonsmith/Desktop/sentient_ai/whispering/whispering.pem')
    # create a new SFTP client
    sftp = ssh.open_sftp()
    # upload the files to the instance
    sftp.put('/Users/canyonsmith/Desktop/sentient_ai/whispering/whispering.py', '/home/ubuntu/whispering/whispering.py')
    sftp.put('/Users/canyonsmith/Desktop/sentient_ai/whispering/requirements.txt', '/home/ubuntu/whispering/requirements.txt')
    # close the SFTP client
    sftp.close()
    # close the SSH client
    ssh.close()
    # print a message to the console
    print('The instance has been started\n')
    # start the program on the instance
    start_program_on_instance(response['instance']['publicIpAddress'])
    return response

def start_program_on_instance(public_ip_address):
    """
    This function starts the program on the instance
    """
    # create a new SSH client
    ssh = paramiko.SSHClient()
    # add the host key
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # connect to the instance
    ssh.connect(hostname=public_ip_address, username='ubuntu', key_filename='/Users/canyonsmith/Desktop/sentient_ai/whispering/whispering.pem')
    # create a new SFTP client
    sftp = ssh.open_sftp()
    # create a new channel
    channel = ssh.invoke_shell()
    # send the command to start the program
    channel.send('python3 whispering.py\n')
    # close the SFTP client
    sftp.close()
    # close the SSH client
    ssh.close()


# write a function that gets the pricing of any aws service using the aws pricing get-products --service-code=
def get_pricing():
    """
    This function gets the pricing of any aws service using the aws pricing get-products --service-code=transcribe
    """
    # create a new pricing client
    client = boto3.client('pricing')
    # get the pricing information
    # first get the service codes for all the services and print them to the console
    response = client.describe_services()['Services']
    # for service in response:
    #     # {'ServiceCode': 'AmazonDAX', 'AttributeNames': ['productFamily', 'memory', 'vcpu', 'instanceType', 'termType', 'usagetype', 'locationType', 'instanceFamily', 'regionCode', 'servicecode', 'currentGeneration', 'networkPerformance', 'location', 'servicename']}
    #     # convert the service code to a string
    #     service_code = str(service['ServiceCode'])
    #     attribute_names = str(service['AttributeNames'])
    #     # print the productFamily 
    #     print(service_code)
    list_of_services = [service['ServiceCode'] for service in response]
    print(list_of_services)
    
    
    for service in list_of_services:
        response = client.get_products(
            ServiceCode=service,
        )
        
        response = response['PriceList'][0]
        # convert the response to a dictionary
        response = eval(response)
        attributes = response['product']['attributes']
        print()
        # operation = attributes['operation']
        # product_family = response['product']['productFamily']
        
        # print(operation, product_family)
        

    response = client.get_products(
        ServiceCode=service_code,
    )
    
    # print the productFamily
    # print the pricing information
    '''{
    "product": {
        "attributes": {
            "groupDescription": "Budgets Reports Distribution",
            "location": "Any",
            "locationType": "AWS Region",
            "operation": "ReportDelivery",
            "servicecode": "AWSBudgets",
            "servicename": "AWS Budgets",
            "usagetype": "BudgetsReports"
        },
        "productFamily": "AWS Budgets",
        "sku": "65GKVXQ58KMKSXD8"
    },
    "publicationDate": "2020-10-15T15:14:42Z",
    "serviceCode": "AWSBudgets",
    "terms": {
        "OnDemand": {
            "65GKVXQ58KMKSXD8.JRTCKXETXF": {
                "effectiveDate": "2020-10-01T00:00:00Z",
                "offerTermCode": "JRTCKXETXF",
                "priceDimensions": {
                    "65GKVXQ58KMKSXD8.JRTCKXETXF.6YS6EN2CT7": {
                        "appliesTo": [],
                        "beginRange": "0",
                        "description": "$0.01 per AWS Budgets Report Delivered",
                        "endRange": "Inf",
                        "pricePerUnit": {
                            "USD": "0.0100000000"
                        },
                        "rateCode": "65GKVXQ58KMKSXD8.JRTCKXETXF.6YS6EN2CT7",
                        "unit": "Message"
                    }
                },
                "sku": "65GKVXQ58KMKSXD8",
                "termAttributes": {}
            }
        }
    },
    "version": "20201015151442"
}'''
#         # print product groupDescription usagetype operation productFamily
    attributes = response['product']['attributes']
    group_description = attributes['groupDescription']
    operation = attributes['operation']
    product_family = response['product']['productFamily']
    
    print(group_description, operation, product_family)
    
    import json
    # get the list of prices
    prices = json.loads(response['PriceList'][0])
    print(json.dumps(prices, indent=4, sort_keys=True))
    return response
    

if __name__ == '__main__':
    if len(sys.argv) > 1:  # if the user gives an argument, then use that as the command to run 
        globals()[sys.argv[1]]()
    else: # else just don't mind it and use the default which is nothing
        command = None


# # accessanalyzer                           | account                                 
# acm                                      | acm-pca                                 
# alexaforbusiness                         | amp                                     
# amplify                                  | amplifybackend                          
# amplifyuibuilder                         | apigateway                              
# apigatewaymanagementapi                  | apigatewayv2                            
# appconfig                                | appconfigdata                           
# appflow                                  | appintegrations                         
# application-autoscaling                  | application-insights                    
# applicationcostprofiler                  | appmesh                                 
# apprunner                                | appstream                               
# appsync                                  | athena                                  
# auditmanager                             | autoscaling                             
# autoscaling-plans                        | backup                                  
# backup-gateway                           | backupstorage                           
# batch                                    | billingconductor                        
# braket                                   | budgets                                 
# ce                                       | chime                                   
# chime-sdk-identity                       | chime-sdk-media-pipelines               
# chime-sdk-meetings                       | chime-sdk-messaging                     
# cloud9                                   | cloudcontrol                            
# clouddirectory                           | cloudformation                          
# cloudfront                               | cloudhsm                                
# cloudhsmv2                               | cloudsearch                             
# cloudsearchdomain                        | cloudtrail                              
# cloudwatch                               | codeartifact                            
# codebuild                                | codecommit                              
# codeguru-reviewer                        | codeguruprofiler                        
# codepipeline                             | codestar                                
# codestar-connections                     | codestar-notifications                  
# cognito-identity                         | cognito-idp                             
# cognito-sync                             | comprehend                              
# comprehendmedical                        | compute-optimizer                       
# connect                                  | connect-contact-lens                    
# connectcampaigns                         | connectparticipant                      
# controltower                             | cur                                     
# customer-profiles                        | databrew                                
# dataexchange                             | datapipeline                            
# datasync                                 | dax                                     
# detective                                | devicefarm                              
# devops-guru                              | directconnect                           
# discovery                                | dlm                                     
# dms                                      | docdb                                   
# drs                                      | ds                                      
# dynamodb                                 | dynamodbstreams                         
# ebs                                      | ec2                                     
# ec2-instance-connect                     | ecr                                     
# ecr-public                               | ecs                                     
# efs                                      | eks                                     
# elastic-inference                        | elasticache                             
# elasticbeanstalk                         | elastictranscoder                       
# elb                                      | elbv2                                   
# emr                                      | emr-containers                          
# emr-serverless                           | es                                      
# events                                   | evidently                               
# finspace                                 | finspace-data                           
# firehose                                 | fis                                     
# fms                                      | forecast                                
# forecastquery                            | frauddetector                           
# fsx                                      | gamelift                                
# gamesparks                               | glacier                                 
# globalaccelerator                        | glue                                    
# grafana                                  | greengrass                              
# greengrassv2                             | groundstation                           
# guardduty                                | health                                  
# healthlake                               | honeycode                               
# iam                                      | identitystore                           
# imagebuilder                             | importexport                            
# inspector                                | inspector2                              
# iot                                      | iot-data                                
# iot-jobs-data                            | iot1click-devices                       
# iot1click-projects                       | iotanalytics                            
# iotdeviceadvisor                         | iotevents                               
# iotevents-data                           | iotfleethub                             
# iotfleetwise                             | iotsecuretunneling                      
# iotsitewise                              | iotthingsgraph                          
# iottwinmaker                             | iotwireless                             
# ivs                                      | ivschat                                 
# kafka                                    | kafkaconnect                            
# kendra                                   | keyspaces                               
# kinesis                                  | kinesis-video-archived-media            
# kinesis-video-media                      | kinesis-video-signaling                 
# kinesisanalytics                         | kinesisanalyticsv2                      
# kinesisvideo                             | kms                                     
# lakeformation                            | lambda                                  
# lex-models                               | lex-runtime                             
# lexv2-models                             | lexv2-runtime                           
# license-manager                          | license-manager-user-subscriptions      
# lightsail                                | location                                
# logs                                     | lookoutequipment                        
# lookoutmetrics                           | lookoutvision                           
# m2                                       | machinelearning                         
# macie                                    | macie2                                  
# managedblockchain                        | marketplace-catalog                     
# marketplace-entitlement                  | marketplacecommerceanalytics            
# mediaconnect                             | mediaconvert                            
# medialive                                | mediapackage                            
# mediapackage-vod                         | mediastore                              
# mediastore-data                          | mediatailor                             
# memorydb                                 | meteringmarketplace                     
# mgh                                      | mgn                                     
# migration-hub-refactor-spaces            | migrationhub-config                     
# migrationhuborchestrator                 | migrationhubstrategy                    
# mobile                                   | mq                                      
# mturk                                    | mwaa                                    
# neptune                                  | network-firewall                        
# networkmanager                           | nimble                                  
# opensearch                               | opsworks                                
# opsworkscm                               | organizations                           
# outposts                                 | panorama                                
# personalize                              | personalize-events                      
# personalize-runtime                      | pi                                      
# pinpoint                                 | pinpoint-email                          
# pinpoint-sms-voice                       | pinpoint-sms-voice-v2                   
# polly                                    | pricing                                 
# privatenetworks                          | proton                                  
# qldb                                     | qldb-session                            
# quicksight                               | ram                                     
# rbin                                     | rds                                     
# rds-data                                 | redshift                                
# redshift-data                            | redshift-serverless                     
# rekognition                              | resiliencehub                           
# resource-groups                          | resourcegroupstaggingapi                
# robomaker                                | rolesanywhere                           
# route53                                  | route53-recovery-cluster                
# route53-recovery-control-config          | route53-recovery-readiness              
# route53domains                           | route53resolver                         
# rum                                      | s3control                               
# s3outposts                               | sagemaker                               
# sagemaker-a2i-runtime                    | sagemaker-edge                          
# sagemaker-featurestore-runtime           | sagemaker-runtime                       
# savingsplans                             | schemas                                 
# sdb                                      | secretsmanager                          
# securityhub                              | serverlessrepo                          
# service-quotas                           | servicecatalog                          
# servicecatalog-appregistry               | servicediscovery                        
# ses                                      | sesv2                                   
# shield                                   | signer                                  
# sms                                      | sms-voice                               
# snow-device-management                   | snowball                                
# sns                                      | sqs                                     
# ssm                                      | ssm-contacts                            
# ssm-incidents                            | sso                                     
# sso-admin                                | sso-oidc                                
# stepfunctions                            | storagegateway                          
# sts                                      | support                                 
# support-app                              | swf                                     
# synthetics                               | textract                                
# timestream-query                         | timestream-write                        
# transcribe                               | transfer                                
# translate                                | voice-id                                
# waf                                      | waf-regional                            
# wafv2                                    | wellarchitected                         
# wisdom                                   | workdocs                                
# worklink                                 | workmail                                
# workmailmessageflow                      | workspaces                              
# workspaces-web                           | xray                                    
# s3api                                    | s3                                      
# configure                                | deploy                                  
# configservice                            | opsworks-cm                             
# runtime.sagemaker                        | history


# Catagories:
Analytics

Application Integration

Blockchain

Business Applications

Cloud Financial Management

Compute

Containers

Database

Developer Tools

End User Computing

Front-End Web & Mobile

Internet of Things

Machine Learning

Management & Governance

Media Services

Migration & Transfer

Networking & Content Delivery

Quantum Technologies

Robotics

Satellite

Security, Identity, & Compliance

Storage



-- Analytics
- athena
- cloudsearch
- cloudsearchdomain
- comprehend
- comprehendmedical
- costandusagereportservice
- cur
- dataexchange
- datapipeline
- detective
- devopsguru



 
AWS Backup
Centralized backup across AWS services
Storage

AWS Storage Gateway
Hybrid storage integration
Storage
 
AWS WAF
Filter malicious web traffic
Security, Identity, & Compliance

AWS Key Management Service (KMS)
Managed creation and control of encryption keys
Security, Identity, & Compliance
 
Amazon Macie
Discover and protect your sensitive data at scale
Security, Identity, & Compliance
 
AWS CloudHSM
Hardware-based key storage for regulatory compliance
Security, Identity, & Compliance
 
AWS Single Sign-On (SSO)
Cloud single sign-on (SSO) service
Security, Identity, & Compliance
 
AWS Resource Access Manager
Simple, secure service to share AWS resources
Security, Identity, & Compliance
Free Trial
Amazon Inspector
Automated and continual vulnerability management for Amazon EC2 and Amazon ECR
Security, Identity, & Compliance
Free Trial
Amazon GuardDuty
Managed threat detection service
Storage
 
AWS Elastic Disaster Recovery (DRS)
Scalable, cost-effective application recovery to AWS

Storage
 
AWS Snow Family
Physical edge computing and storage devices for rugged or disconnected environments
Storage
 
Amazon FSx
Launch, run, and scale feature-rich and highly-performant file systems with just a few clicks
Storage
 
Amazon S3 Glacier
Low-cost archive storage in the cloud
Storage
12 Months Free
Amazon Elastic File System (EFS)
Fully managed file system for EC2
Storage
12 Months Free
Amazon Elastic Block Store (EBS)
EC2 block storage volumes
Storage
Free Trial
Amazon Simple Storage Service (S3)
Object storage built to retrieve any amount of data from anywhere

Quantum Technologies
Free Trial
Amazon Braket
Accelerate quantum computing research
Robotics
Free Trial
AWS RoboMaker
Develop, test, and deploy robotics applications
Satellite
 
AWS Ground Station
Fully managed ground station as a service
Security, Identity, & Compliance
Free Trial
Amazon Detective
Investigate potential security issues
Security, Identity, & Compliance
 
AWS Identity and Access Management
Securely manage access to services and resources
Security, Identity, & Compliance
 
AWS Certificate Manager
Manager Provision, manage, and deploy SSL/TLS certificates
Security, Identity, & Compliance
 
AWS Artifact
On-demand access to AWS’ compliance reports
Security, Identity, & Compliance
 
AWS Network Firewall
Deploy network security across your Amazon VPCs with just a few clicks
Security, Identity, & Compliance
 
AWS Shield
DDoS protection
Security, Identity, & Compliance
 
Amazon Cognito
Identity management for your apps
Security, Identity, & Compliance
 
AWS Firewall Manager
Central management of firewall rules
Security, Identity, & Compliance
 
AWS Audit Manager
Continuously audit your AWS usage to simplify how you assess risk and compliance
Security, Identity, & Compliance
Free Trial
AWS Secrets Manager
Rotate, manage, and retrieve secrets
Security, Identity, & Compliance
 
AWS Directory Service
Host and manage active directory

Migration
Always Free
AWS Application Migration Service (MGN)
Automate application migration and modernization

Migration
 
AWS Migration Hub
Track migrations from a single place
Networking & Content Delivery
 
AWS Global Accelerator
Improve global application availability and performance
Networking & Content Delivery
 
AWS PrivateLink
Securely access services hosted on AWS
Networking & Content Delivery
 
AWS Private 5G
Easily deploy, manage, and scale a private cellular network
Networking & Content Delivery
 
AWS Cloud Map
Service discovery for cloud resources
Networking & Content Delivery
 
Amazon Route 53
53 Scalable domain name system (DNS)
Networking & Content Delivery
12 Months Free
Elastic Load Balancing (ELB)
Distribute incoming traffic across multiple targets
Networking & Content Delivery
 
AWS VPN
Securely access your network resources
Networking & Content Delivery
 
AWS App Mesh
Monitor and control microservices
Networking & Content Delivery
 
AWS Transit Gateway
Easily scale VPC and account connections
Networking & Content Delivery
12 Months Free
Amazon CloudFront
Global content delivery network
Networking & Content Delivery
 
AWS Direct Connect
Dedicated network connection to AWS
Networking & Content Delivery
 
AWS Cloud WAN (Preview)
Easily build, manage, and monitor global wide area networks
Networking & Content Delivery
 
Amazon VPC
Isolated cloud resources

Media Services
 
AWS Elemental MediaTailor
Video personalization and monetization
Media Services
 
AWS Elemental Appliances & Software
On-premises media solutions
Media Services
 
Amazon Elastic Transcoder
Easy-to-use scalable media transcoding
Media Services
 
AWS Elemental MediaStore
Media storage and simple http origin
Media Services
 
Amazon Interactive Video Service
Build engaging live stream experiences
Media Services
 
AWS Elemental MediaConvert
Convert file-based video content
Media Services
 
AWS Elemental MediaConnect
Reliable and secure live video transport
Media Services
 
AWS Elemental MediaLive
Convert live video content
Migration
 
AWS Database Migration Service (DMS)
Migrate databases with minimal downtime
Migration
AWS Mainframe Modernization
Migrate, modernize, operate, and run mainframe workloads

Migration
 
Migration Evaluator (formerly TSO Logic)
Create a business case for cloud migration
Migration
 
AWS Transfer Family
Fully managed SFTP, FTPS, and FTP service
Migration
 
AWS Server Migration Service (SMS)
Migrate on-premises servers to AWS
Migration
 
AWS DataSync
Simple, fast, online data transfer
Migration
Free Trial
AWS Application Discovery Service
Discover on-premises applications to streamline migration

Management & Governance
 
AWS CloudFormation
Create and manage resources with templates
Management & Governance
AWS Service Management Connector
Provision, manage and operate AWS resources within Service Management Tools

Management & Governance
 
AWS Proton
Automate management for container and serverless deployments
Management & Governance
 
AWS Management Console Mobile Application
Access resources on the go
Management & Governance
 
AWS OpsWorks
Automate operations with Chef and Puppet
Management & Governance
 
AWS Chatbot
ChatOps for AWS
Management & Governance
 
AWS Control Tower
Set up and govern a secure, compliant multi-account environment
Management & Governance
 
AWS Trusted Advisor
Optimize performance and security
Management & Governance
 
AWS Resilience Hub
Prepare and protect your applications from disruptions
Management & Governance
 
AWS Launch Wizard
Easily size, configure, and deploy third party applications on AWS
Management & Governance
 
AWS Personal Health Dashboard
Personalized view of AWS service health
Management & Governance
 
AWS Service Catalog
Create and use standardized products
Media Services
 
Amazon Kinesis Video Streams
Process and analyze video streams
Media Services
 
AWS Elemental MediaPackage
Video origination and packaging
Media Services
 
Amazon Nimble Studio
Accelerate content creation in the cloud

Machine Learning
Free Trial
Amazon SageMaker Ground Truth
Build accurate ML training datasets
Machine Learning
12 Months Free
Amazon Rekognition
Analyze image and video
Machine Learning
12 Months Free
Amazon Polly
Turn text into life-like speech
Machine Learning
12 Months Free
Amazon Comprehend
Discover insights and relationships in text
Management & Governance
 
Amazon Managed Service for Prometheus
Highly available, secure, and managed monitoring for your containers
Management & Governance
 
AWS Distro for OpenTelemetry
Secure, production-ready open source distribution with predictable performance
Management & Governance
 
AWS Managed Services
Infrastructure operations management for AWS
Management & Governance
 
AWS Organizations
Central governance and management across AWS accounts
Management & Governance
 
Amazon CloudWatch
Monitor resources and applications
Management & Governance
 
Amazon Managed Grafana
Scalable, secure, and highly available data visualization for your operational metrics, logs, and traces
Management & Governance
 
AWS CloudTrail
Track user activity and API usage
Management & Governance
 
AWS Management Console
Web-based user interface
Management & Governance
 
AWS License Manager
Track, manage, and control licenses
Management & Governance
 
AWS Config
Track resources inventory and changes
Management & Governance
 
AWS Systems Manager
Gain operational insights and take action

Machine Learning
 
AWS Panorama
Improve your operations with computer vision at the edge
Machine Learning
Free Trial
Amazon Kendra
Reinvent enterprise search with ML
Machine Learning
Free Trial
Amazon Forecast
Increase forecast accuracy using machine learning
Machine Learning
 
Amazon CodeGuru
Find your most expensive lines of code
Machine Learning
 
AWS Inferentia
Machine learning inference chip
Machine Learning
 
AWS DeepLens
Deep learning enabled video camera
Machine Learning
 
Amazon Transcribe
Automatic speech recognition
Machine Learning
 
Apache MXNet on AWS
Scalable, open-source deep learning framework
Machine Learning
 
AWS Deep Learning AMIs
Deep learning on Amazon EC2
Machine Learning
 
Amazon Translate
Natural and fluent language translation
Machine Learning
 
Amazon Elastic Inference
Deep learning inference acceleration
Machine Learning
Free Trial
Amazon Augmented AI
Easily implement human review of ML predictions
Machine Learning
Free Trial
Amazon Lookout for Equipment
Detect abnormal equipment behavior by analyzing sensor data
Machine Learning
 
PyTorch on AWS
Flexible open-source machine learning framework
Machine Learning
Free Trial
AWS DeepRacer
Autonomous 1/18th scale race car, driven by ML

Internet Of Things
 
AWS IoT 1-Click
One click creation of an AWS Lambda trigger
Internet Of Things
 
AWS IoT SiteWise
IoT data collector and interpreter
Machine Learning
 
Amazon Monitron
Reduce unplanned equipment downtime with predictive maintenance and machine learning
Machine Learning
 
TensorFlow on AWS
Open-source machine intelligence library
Machine Learning
Free Trial
Amazon Lookout for Metrics
Automatically detect anomalies in metrics and identify their root cause
Machine Learning
Free Trial
Amazon DevOps Guru
ML-powered cloud operations service to improve application availability
Machine Learning
Free Trial
Amazon SageMaker
Build, train, and deploy machine learning models at scale
Machine Learning
 
Amazon Lex
Build voice and text chatbots
Machine Learning
 
AWS DeepComposer
ML enabled musical keyboard
Machine Learning
Free Trial
Amazon Textract
Extract text and data from documents
Machine Learning
 
Amazon HealthLake
Securely store, transform, query, and analyze health data in minutes
Machine Learning
 
AWS Deep Learning Containers
Docker images for deep learning
Machine Learning
Free Trial
Amazon Personalize
Build real-time recommendations into your applications
Machine Learning
Free Trial
Amazon Lookout for Vision
Spot product defects using computer vision to automate quality inspection
Machine Learning
Free Trial
Amazon Fraud Detector
Detect more online fraud faster


Game Tech
 
Amazon Lumberyard
A free cross-platform 3D game engine, with Full Source, integrated with AWS and Twitch
Game Tech
 
Amazon GameLift
Simple, fast, cost-effective dedicated game server hosting
Internet Of Things
 
AWS Partner Device Catalog
Curated catalog of AWS-compatible IoT hardware
Internet Of Things
 
AWS IoT Analytics
Analytics for IoT devices
Internet Of Things
12 Months Free
AWS IoT Greengrass
Local compute, messaging, and sync for devices
Internet Of Things
 
AWS IoT FleetWise
Easily collect, transform, and transfer vehicle data to the cloud in near-real time
Internet Of Things
 
AWS IoT TwinMaker
Optimize operations by easily creating digital twins of real-world systems
Internet Of Things
 
FreeRTOS
Real-time operating system for microcontrollers
Internet Of Things
12 Months Free
AWS IoT Device Management
Onboard, organize, and remotely manage IoT devices
Internet Of Things
 
AWS IoT EduKit
Learn how to build simple IoT applications with reference hardware and step-by-step tutorials
Internet Of Things
 
AWS IoT Button
Cloud programmable dash button
Internet Of Things
 
AWS IoT RoboRunner
Build applications that help fleets of robots work together seamlessly
Internet Of Things
 
AWS IoT Core
Connect devices to the cloud
Internet Of Things
 
AWS IoT Events
IoT event detection and response


Developer Tools
 
AWS CodeArtifact
Secure, scalable, and cost-effective artifact management for software development
Developer Tools
 
AWS CodePipeline
Release software using continuous delivery
Developer Tools
 
Amazon Corretto
Production-ready distribution of OpenJDK
Developer Tools
 
AWS X-Ray
Analyze and debug your applications
Developer Tools
 
AWS CloudShell
Command line access to AWS resources and tools directly from a browser
Developer Tools
 
AWS Fault Injection Simulator
Improve resiliency and performance with controlled experiments
End User Computing
 
Amazon WorkSpaces
Virtual desktops in the cloud
End User Computing
Free Trial
Amazon AppStream 2.0
Stream desktop applications securely to a browser
Front-End Web & Mobile
Free Trial
AWS AppSync
Accelerate app development with fully-managed, scalable GraphQL APIs
Front-End Web & Mobile
Amazon Simple Email Service (SES)
High-scale inbound and outbound email

Front-End Web & Mobile
Free Trial
Amazon API Gateway
Build, deploy, and manage APIs
Front-End Web & Mobile
Free Trial
AWS Device Farm
Test Android, iOS, and web apps on real devices in the AWS cloud
Front-End Web & Mobile
Amazon Pinpoint
Multichannel marketing communications

Front-End Web & Mobile
Free Trial
Amazon Location Service
Securely and easily add location data to applications
Front-End Web & Mobile
Free Trial
AWS Amplify
Build, deploy, host, and manage scalable web and mobile apps

Game Tech
 
Amazon Lumberyard
A free cross-platform 3D game engine, with Full Source, integrated with AWS and Twitch
Game Tech
 
Amazon GameLift
Simple, fast, cost-effective dedicated game server hosting
Internet Of Things
 
AWS Partner Device Catalog
Curated catalog of AWS-compatible IoT hardware
Internet Of Things
 
AWS IoT Analytics
Analytics for IoT devices
Internet Of Things
12 Months Free
AWS IoT Greengrass
Local compute, messaging, and sync for devices
Internet Of Things
 
AWS IoT FleetWise
Easily collect, transform, and transfer vehicle data to the cloud in near-real time
Internet Of Things
 
AWS IoT TwinMaker
Optimize operations by easily creating digital twins of real-world systems
Internet Of Things
 
FreeRTOS
Real-time operating system for microcontrollers
Internet Of Things
12 Months Free
AWS IoT Device Management
Onboard, organize, and remotely manage IoT devices
Internet Of Things
 
AWS IoT EduKit
Learn how to build simple IoT applications with reference hardware and step-by-step tutorials
Internet Of Things
 
AWS IoT Button
Cloud programmable dash button
Internet Of Things
 
AWS IoT RoboRunner
Build applications that help fleets of robots work together seamlessly
Internet Of Things
 
AWS IoT Core
Connect devices to the cloud
Internet Of Things
 
AWS IoT Events
IoT event detection and response
Internet Of Things
 
AWS IoT Device Defender
Security management for IoT devices


Databases
Free Trial
Amazon MemoryDB for Redis
Redis-compatible, durable, in-memory database service for ultra-fast performance

Databases
 
Amazon Aurora
High performance managed relational database
Databases
Free Trial
Amazon Neptune
Fully managed graph database service

Databases
Free Trial
Amazon ElastiCache
In-memory caching service
Databases
Free Trial
Amazon Keyspaces (for Apache Cassandra)
Managed Cassandra-compatible database
Databases
Free Trial
Amazon Redshift
Fast, simple, cost-effective data warehousing
Developer Tools
 
AWS CodeDeploy
Automate code deployments
Developer Tools
 
AWS Cloud Development Kit (CDK)
Model cloud infrastructure using code
Developer Tools
 
AWS Cloud9
Write, run, and debug code on a cloud IDE
Developer Tools
 
AWS Command Line Interface (CLI)
Line Interface Unified tool to manage AWS services
Developer Tools
 
AWS Tools and SDKs
Tools and SDKs for AWS
Developer Tools
 
AWS CodeStar
Develop and deploy AWS applications
Developer Tools
 
AWS CodeBuild
Build and test code
Developer Tools
 
AWS Cloud Control API
Manage AWS and third-party cloud infrastructure with consistent APIs
Developer Tools
 
AWS CodeCommit
Store code in private Git repositories


Compute
 
AWS Wavelength
Deliver ultra-low latency applications for 5G devices
Compute
 
AWS Auto Scaling
Scale multiple resources to meet demand
Compute
 
AWS Outposts
Run AWS infrastructure on-premises
Compute
Free Trial
Amazon Lightsail
Launch and manage virtual private servers
Containers
 
AWS Fargate
Serverless compute for containers
Containers
 
Amazon Elastic Kubernetes Service (EKS)
The most trusted way to run Kubernetes
Containers
 
Red Hat OpenShift Service on AWS
Managed OpenShift in the cloud
Containers
 
AWS App2Container
Containerize and migrate existing applications
Containers
Free Trial
Amazon Elastic Container Registry (ECR)
Easily store, manage, and deploy container images
Containers
 
AWS Copilot
AWS Copilot is the easiest way to launch and manage your containerized application on AWS
Containers
 
Amazon Elastic Container Service (ECS)
Highly secure, reliable, and scalable way to run containers
Databases
 
Amazon Timestream
Fully managed time series database
Databases
Free Trial
Amazon DynamoDB
Managed NoSQL database
Databases
Free Trial
Amazon DocumentDB
Fully managed document database

Databases
Free Trial
Amazon RDS
Managed relational database service for MySQL, PostgreSQL, Oracle, SQL Server, and MariaDB


Cloud Financial Management
 
Savings Plans
Save up to 72% on compute usage with flexible pricing
Cloud Financial Management
 
Reserved Instance (RI) Reporting
Dive deeper into your reserved instances (RIs)
Cloud Financial Management
 
AWS Cost and Usage Report
Access comprehensive cost and usage information
Cloud Financial Management
 
AWS Cost Explorer
Analyze your AWS cost and usage
Cloud Financial Management
 
AWS Budgets
Set custom cost and usage budgets
Compute
 
AWS Compute Optimizer
Identify optimal AWS Compute resources
Compute
 
AWS App Runner
Production web applications at scale made easy for developers
Compute
 
VMware Cloud on AWS
Build a hybrid cloud without custom hardware
Compute
 
AWS Serverless Application Repository
Discover, deploy, and publish serverless applications
Compute
 
Amazon EC2 Auto Scaling
Scale compute capacity to meet demand
Compute
 
AWS Elastic Beanstalk
Run and manage web apps
Compute
Free Trial
AWS Lambda
Run code without thinking about servers
Compute
 
AWS Batch
Run batch jobs at any scale
Compute
Free Trial
Amazon EC2
Virtual servers in the cloud
Compute
 
Amazon EC2 Spot Instances
Run workloads for up to 90% off


Application Integration
 
Amazon Simple Notification Service (SNS)
Pub/sub, SMS, email, and mobile push notifications
Application Integration
 
Amazon AppFlow
No-code integration for SaaS apps & AWS services
Application Integration
 
Amazon Simple Queue Service (SQS)
Managed message queues
Application Integration
 
AWS Step Functions
Coordination for distributed applications
Application Integration
 
Amazon MQ
Managed message broker service
Architecture Strategy
 
AWS Well-Architected Tool
Review and improve your workloads
Blockchain
 
Amazon Managed Blockchain
Create and manage scalable blockchain networks
Blockchain
 
Amazon Quantum Ledger Database (QLDB)
Fully managed ledger database
Business Applications
Amazon WorkMail
Secure email and calendaring

Business Applications
Free Trial
Amazon WorkDocs
Secure enterprise document storage and sharing

Business Applications
Alexa for Business
Empower your organization with Alexa

Business Applications
Amazon Connect
Omnichannel cloud contact center

Business Applications
Amazon Honeycode
Build mobile & web apps without programming

Business Applications
Amazon Chime
Frustration-free meetings, video calls, and chat

Business Applications
Amazon Chime SDK
Real-time messaging, audio, video, and screen sharing 


AR & VR
 
Amazon Sumerian
Build and run AR and VR applications
Analytics
Free Trial
AWS Glue
Simple, scalable, and serverless data integration
Analytics
 
Amazon Athena
Query data in S3 using SQL
Analytics
Free Trial
Amazon OpenSearch Service (successor to Amazon Elasticsearch Service)
Search, visualize, and analyze up to petabytes of text and unstructured data
Analytics
 
AWS Data Pipeline
Orchestration service for periodic, data-driven workflows
Analytics
 
Amazon FinSpace
Store, catalog, prepare, and analyze financial industry data in minutes
Analytics
 
AWS Lake Formation
Build a secure data lake in days
Analytics
 
Amazon EMR
Hosted Hadoop framework
Analytics
 
Amazon CloudSearch
Managed search service
Analytics
 
Amazon Kinesis
Analyze real-time video and data streams
Analytics
 
AWS Data Exchange
Find, subscribe to, and use third-party data in the cloud
Analytics
Free Trial
Amazon QuickSight
Fast business analytics service
Analytics
 
Amazon Managed Streaming for Apache Kafka (MSK)
Fully managed Apache Kafka service
Application Integration
 
Amazon Managed Workflows for Apache Airflow (MWAA)
Highly available, secure, and managed workflow orchestration for Apache Airflow
Application Integration
 
Amazon EventBridge
Serverless event bus for SaaS apps & AWS services



AWS Backup,Centralized backup across AWS services,Storage
AWS Storage Gateway,Hybrid storage integration,Storage
AWS WAF,Filter malicious web traffic,Security Identity & Compliance
AWS Key Management Service (KMS),Managed creation and control of encryption keys,Security Identity & Compliance
Amazon Macie,Discover and protect your sensitive data at scale,Security Identity & Compliance
AWS CloudHSM,Hardware-based key storage for regulatory compliance,Security Identity & Compliance
AWS Single Sign-On (SSO),Cloud single sign-on (SSO) service,Security Identity & Compliance
AWS Resource Access Manager,Simple, secure service to share AWS resources,Security Identity & Compliance
Amazon Inspector,Automated and continual vulnerability management for Amazon EC2 and Amazon ECR,Security Identity & Compliance
Amazon GuardDuty,Managed threat detection service,Storage
AWS Elastic Disaster Recovery (DRS),Scalable, cost-effective application recovery to AWS,Storage
AWS Snow Family,Physical edge computing and storage devices for rugged or disconnected environments,Storage
Amazon FSx,Launch, run, and scale feature-rich and highly-performant file systems with just a few clicks,Storage
Amazon S3 Glacier,Low-cost archive storage in the cloud,Storage
Amazon Elastic File System (EFS),Fully managed file system for EC2,Storage
Amazon Elastic Block Store (EBS),EC2 block storage volumes,Storage
Amazon Simple Storage Service (S3),Object storage built to retrieve any amount of data from anywhere,Quantum Technologies
Amazon Braket,Accelerate quantum computing research,Robotics
AWS RoboMaker,Develop, test, and deploy robotics applications,Satellite
AWS Ground Station,Fully managed ground station as a service,Security Identity & Compliance
Amazon Detective,Investigate potential security issues,Security Identity & Compliance
AWS Identity and Access Management,Securely manage access to services and resources,Security Identity & Compliance
AWS Certificate Manager,Manager Provision, manage, and deploy SSL/TLS certificates,Security Identity & Compliance
AWS Artifact,On-demand access to AWS’ compliance reports,Security Identity & Compliance
AWS Network Firewall,Deploy network security across your Amazon VPCs with just a few clicks,Security Identity & Compliance
AWS Shield,DDoS protection,Security Identity & Compliance
Amazon Cognito,Identity management for your apps,Security Identity & Compliance
AWS Firewall Manager,Central management of firewall rules,Security Identity & Compliance
AWS Secrets Manager,Rotate, manage, and retrieve secrets,Security Identity & Compliance
AWS Directory Service,Host and manage active directory,Security Identity & Compliance
AWS Database Migration Service (DMS),Migrate databases with minimal downtime,Migration
AWS Mainframe Modernization,Migrate, modernize, operate, and run mainframe workloads,Migration
Migration Evaluator (formerly TSO Logic),Create a business case for cloud migration,Migration
AWS Transfer Family,Fully managed SFTP, FTPS, and FTP service,Migration
AWS Server Migration Service (SMS),Migrate on-premises servers to AWS,Migration
AWS DataSync,Simple, fast, online data transfer,Migration
AWS CloudFormation,Create and manage resources with templates,Management & Governance
AWS Service Management Connector,Provision, manage and operate AWS resources within Service Management Tools,Management & Governance
AWS Proton,Automate management for container and serverless deployments,Management & Governance
AWS Chatbot,ChatOps for AWS,Management & Governance
AWS Control Tower,Set up and govern a secure, compliant multi-account environment,Management & Governance
AWS Trusted Advisor,Optimize performance and security,Management & Governance
AWS Resilience Hub,Prepare and protect your applications from disruptions,Management & Governance
AWS Launch Wizard,Easily size, configure, and deploy third party applications on AWS,Management & Governance
AWS Personal Health Dashboard,Personalized view of AWS service health,Management & Governance
AWS Service Catalog,Create and use standardized products,Management & Governance
Amazon Kinesis Video Streams,Process and analyze video streams,Media Services
AWS Elemental MediaTailor,Video personalization and monetization,Media Services
AWS Elemental Appliances & Software,On-premises media solutions,Media Services
Amazon Elastic Transcoder,Easy-to-use scalable media transcoding,Media Services
AWS Elemental MediaStore,Media storage and simple http origin,Media Services
Amazon Interactive Video Service,Build engaging live stream experiences,Media Services
AWS Elemental MediaConvert,Convert file-based video content,Media Services
AWS Elemental MediaConnect,Reliable and secure live video transport,Media Services
AWS Elemental MediaLive,Convert live video content,Media Services
Amazon SageMaker Ground Truth,Build accurate ML training datasets,Machine Learning
Amazon Rekognition,Analyze image and video,Machine Learning
Amazon Polly,Turn text into life-like speech,Machine Learning
Amazon Comprehend,Discover insights and relationships in text,Machine Learning
Amazon Managed Service for Prometheus,Highly available, secure, and managed monitoring for your containers,Management & Governance
AWS Distro for OpenTelemetry,Secure, production-ready open source distribution with predictable performance,Management & Governance
AWS Managed Services,Infrastructure operations management for AWS,Management & Governance
AWS Organizations,Central governance and management across AWS accounts,Management & Governance
Amazon CloudWatch,Monitor resources and applications,Management & Governance
Amazon Managed Grafana,Scalable, secure, and highly available data visualization for your operational metrics, logs, and traces,Management & Governance
AWS CloudTrail,Track user activity and API usage,Management & Governance
AWS Management Console,Web-based user interface,Management & Governance
AWS License Manager,Track, manage, and control licenses,Management & Governance
AWS Config,Track resources inventory and changes,Management & Governance
AWS Systems Manager,Gain operational insights and take action,Management & Governance
AWS Panorama,Improve your operations with computer vision at the edge,Machine Learning
Amazon Kendra,Reinvent enterprise search with ML,Machine Learning
Amazon Forecast,Increase forecast accuracy using machine learning,Machine Learning
Amazon CodeGuru,Find your most expensive lines of code,Machine Learning
AWS Inferentia,Machine learning inference chip,Machine Learning
AWS DeepLens,Deep learning enabled video camera,Machine Learning
Amazon Transcribe,Automatic speech recognition,Machine Learning
Apache MXNet on AWS,Scalable, open-source deep learning framework,Machine Learning
AWS Deep Learning AMIs,Deep learning on Amazon EC2,Machine Learning
Amazon Translate,Natural and fluent language translation,Machine Learning
Amazon Elastic Inference,Deep learning inference acceleration,Machine Learning
Amazon Augmented AI,Easily implement human review of ML predictions,Machine Learning
Amazon Lookout for Equipment,Detect abnormal equipment behavior by analyzing sensor data,Machine Learning
PyTorch on AWS,Flexible open-source machine learning framework,Machine Learning
AWS DeepRacer,Autonomous 1/18th scale race car, driven by ML,Machine Learning
AWS IoT 1-Click,One click creation of an AWS Lambda trigger,Internet Of Things
AWS IoT SiteWise,IoT data collector and interpreter,Machine Learning
Amazon Monitron,Reduce unplanned equipment downtime with predictive maintenance and machine learning,Machine Learning
TensorFlow on AWS,Open-source machine intelligence library,Machine Learning
Amazon Lookout for Metrics,Automatically detect anomalies in metrics and identify their root cause,Machine Learning
Amazon DevOps Guru,ML-powered cloud operations service to improve application availability,Machine Learning
Amazon SageMaker,Build, train, and deploy machine learning models at scale,Machine Learning
Amazon Lex,Build voice and text chatbots,Machine Learning
AWS DeepComposer,ML enabled musical keyboard,Machine Learning
Amazon Textract,Extract text and data from documents,Machine Learning
Amazon HealthLake,Securely store, transform, query, and analyze health data in minutes,Machine Learning
AWS Deep Learning Containers,Docker images for deep learning,Machine Learning
Amazon Personalize,Build real-time recommendations into your applications,Machine Learning
Amazon Lookout for Vision,Spot product defects using computer vision to automate quality inspection,Machine Learning
Amazon Fraud Detector,Detect more online fraud faster,Machine Learning
Amazon Lumberyard,A free cross-platform 3D game engine, with Full Source, integrated with AWS and Twitch,Game Tech
Amazon GameLift,Simple, fast, cost-effective dedicated game server hosting,Internet Of Things
AWS Partner Device Catalog,Curated catalog of AWS-compatible IoT hardware,Internet Of Things
AWS IoT Analytics,Analytics for IoT devices,Internet Of Things
AWS IoT Greengrass,Local compute, messaging, and sync for devices,Internet Of Things
AWS IoT FleetWise,Easily collect, transform, and transfer vehicle data to the cloud in near-real time,Internet Of Things
AWS IoT TwinMaker,Optimize operations by easily creating digital twins of real-world systems,Internet Of Things
FreeRTOS,Real-time operating system for microcontrollers,Internet Of Things
AWS IoT Device Management,Onboard, organize, and remotely manage IoT devices,Internet Of Things
AWS IoT EduKit,Learn how to build simple IoT applications with reference hardware and step-by-step tutorials,Internet Of Things
AWS IoT Button,Cloud programmable dash button,Internet Of Things
AWS IoT RoboRunner,Build applications that help fleets of robots work together seamlessly,Internet Of Things
AWS IoT Core,Connect devices to the cloud,Internet Of Things
AWS IoT Events,IoT event detection and response,Internet Of Things
AWS CodeArtifact,Secure, scalable, and cost-effective artifact management for software development,Developer Tools
AWS CodePipeline,Release software using continuous delivery,Developer Tools
Amazon Corretto,Production-ready distribution of OpenJDK,Developer Tools
AWS X-Ray,Analyze and debug your applications,Developer Tools
AWS CloudShell,Command line access to AWS resources and tools directly from a browser,Developer Tools
AWS Fault Injection Simulator,Improve resiliency and performance with controlled experiments,End User Computing
Amazon WorkSpaces,Virtual desktops in the cloud,End User Computing
Amazon AppStream 2.0,Stream desktop applications securely to a browser,Front-End Web & Mobile
AWS AppSync,Accelerate app development with fully-managed, scalable GraphQL APIs,Front-End Web & Mobile
Amazon Simple Email Service (SES),High-scale inbound and outbound email,Front-End Web & Mobile
Amazon API Gateway,Build, deploy, and manage APIs,Front-End Web & Mobile
AWS Device Farm,Test Android, iOS, and web apps on real devices in the AWS cloud,Front-End Web & Mobile
Amazon Pinpoint,Multichannel marketing communications,Front-End Web & Mobile
Amazon Location Service,Securely and easily add location data to applications,Front-End Web & Mobile
AWS Amplify,Build, deploy, host, and manage scalable web and mobile apps,Game Tech
AWS Cloud Development Kit (CDK),Model cloud infrastructure using code,Developer Tools
AWS Cloud9,Write, run, and debug code on a cloud IDE,Developer Tools
AWS Command Line Interface (CLI),Line Interface Unified tool to manage AWS services,Developer Tools
AWS Tools and SDKs,Tools and SDKs for AWS,Developer Tools
AWS CodeStar,Develop and deploy AWS applications,Developer Tools
AWS CodeBuild,Build and test code,Developer Tools
AWS Cloud Control API,Manage AWS and third-party cloud infrastructure with consistent APIs,Developer Tools
AWS CodeCommit,Store code in private Git repositories,Compute
AWS Wavelength,Deliver ultra-low latency applications for 5G devices,Compute
AWS Auto Scaling,Scale multiple resources to meet demand,Compute
AWS Outposts,Run AWS infrastructure on-premises,Compute
Amazon Lightsail,Launch and manage virtual private servers,Containers
AWS Fargate,Serverless compute for containers,Containers
Amazon Elastic Kubernetes Service (EKS),The most trusted way to run Kubernetes,Containers
Red Hat OpenShift Service on AWS,Managed OpenShift in the cloud,Containers
AWS App2Container,Containerize and migrate existing applications,Containers
Amazon Elastic Container Registry (ECR),Easily store, manage, and deploy container images,Containers
AWS Copilot,AWS Copilot is the easiest way to launch and manage your containerized application on AWS,Containers
Amazon Elastic Container Service (ECS),Highly secure, reliable, and scalable way to run containers,Databases
Amazon Timestream,Fully managed time series database,Databases
Amazon DynamoDB,Managed NoSQL database,Databases
Amazon DocumentDB,Fully managed document database,Databases
Amazon RDS,Managed relational database service for MySQL, PostgreSQL, Oracle, SQL Server, and MariaDB,Databases
Savings Plans,Save up to 72% on compute usage with flexible pricing,Cloud Financial Management
Reserved Instance (RI) Reporting,Dive deeper into your reserved instances (RIs),Cloud Financial Management
AWS Cost and Usage Report,Access comprehensive cost and usage information,Cloud Financial Management
AWS Cost Explorer,Analyze your AWS cost and usage,Cloud Financial Management
AWS Budgets,Set custom cost and usage budgets,Cloud Financial Management
AWS Compute Optimizer,Identify optimal AWS Compute resources,Compute
AWS App Runner,Production web applications at scale made easy for developers,Compute
VMware Cloud on AWS,Build a hybrid cloud without custom hardware,Compute
AWS Serverless Application Repository,Discover, deploy, and publish serverless applications,Compute
AWS Elastic Beanstalk,Run and manage web apps,Compute
AWS Lambda,Run code without thinking about servers,Compute
AWS Batch,Run batch jobs at any scale,Compute
Amazon EC2,Virtual servers in the cloud,Compute
Amazon EC2 Spot Instances,Run workloads for up to 90% off,Compute
Amazon Simple Notification Service (SNS),Pub/sub, SMS, email, and mobile push notifications,Application Integration
Amazon AppFlow,No-code integration for SaaS apps & AWS services,Application Integration
Amazon Simple Queue Service (SQS),Managed message queues,Application Integration
AWS Step Functions,Coordination for distributed applications,Application Integration
Amazon MQ,Managed message broker service,Architecture Strategy
AWS Well-Architected Tool,Review and improve your workloads,Blockchain
Amazon Managed Blockchain,Create and manage scalable blockchain networks,Blockchain
Amazon Quantum Ledger Database (QLDB),Fully managed ledger database,Business Applications
Amazon WorkMail,Secure email and calendaring,Business Applications
Amazon WorkDocs,Secure enterprise document storage and sharing,Business Applications
Alexa for Business,Empower your organization with Alexa,Business Applications
Amazon Connect,Omnichannel cloud contact center,Business Applications
Amazon Honeycode,Build mobile & web apps without programming,Business Applications
Amazon Chime,Frustration-free meetings, video calls, and chat,Business Applications
Amazon Chime SDK,Real-time messaging, audio, video, and screen sharing,Business Applications
Amazon Sumerian,Build and run AR and VR applications,AR & VR
AWS Glue,Simple, scalable, and serverless data integration,Analytics
Amazon Athena,Query data in S3 using SQL,Analytics
Amazon OpenSearch Service (successor to Amazon Elasticsearch Service),Search, visualize, and analyze up to petabytes of text and unstructured data,Analytics
AWS Data Pipeline,Orchestration service for periodic, data-driven workflows,Analytics
Amazon FinSpace,Store, catalog, prepare, and analyze financial industry data in minutes,Analytics
AWS Lake Formation,Build a secure data lake in days,Analytics
Amazon EMR,Hosted Hadoop framework,Analytics
Amazon CloudSearch,Managed search service,Analytics
Amazon Kinesis,Analyze real-time video and data streams,Analytics
AWS Data Exchange,Find, subscribe to, and use third-party data in the cloud,Analytics
Amazon QuickSight,Fast business analytics service,Analytics
Amazon Managed Streaming for Apache Kafka (MSK),Fully managed Apache Kafka service,Application Integration
Amazon Managed Workflows for Apache Airflow (MWAA),Highly available, secure, and managed workflow orchestration for Apache Airflow,Application Integration
Amazon EventBridge,Serverless event bus for SaaS apps & AWS services









Amazon Kinesis Video Streams,Process and analyze video streams,Media Services
AWS Elemental MediaTailor,Video personalization and monetization,Media Services
AWS Elemental Appliances & Software,On-premises media solutions,Media Services
Amazon Elastic Transcoder,Easy-to-use scalable media transcoding,Media Services
AWS Elemental MediaStore,Media storage and simple http origin,Media Services
Amazon Interactive Video Service,Build engaging live stream experiences,Media Services
AWS Elemental MediaConvert,Convert file-based video content,Media Services
AWS Elemental MediaConnect,Reliable and secure live video transport,Media Services
AWS Elemental MediaLive,Convert live video content,Media Services
Amazon SageMaker Ground Truth,Build accurate ML training datasets,Machine Learning
Amazon Rekognition,Analyze image and video,Machine Learning
Amazon Polly,Turn text into life-like speech,Machine Learning
Amazon Comprehend,Discover insights and relationships in text,Machine Learning
Amazon Managed Service for Prometheus,Highly available, secure, and managed monitoring for your containers,Management & Governance
AWS Distro for OpenTelemetry,Secure, production-ready open source distribution with predictable performance,Management & Governance
AWS Managed Services,Infrastructure operations management for AWS,Management & Governance
AWS Organizations,Central governance and management across AWS accounts,Management & Governance
Amazon CloudWatch,Monitor resources and applications,Management & Governance
Amazon Managed Grafana,Scalable, secure, and highly available data visualization for your operational metrics, logs, and traces,Management & Governance
AWS CloudTrail,Track user activity and API usage,Management & Governance
AWS Management Console,Web-based user interface,Management & Governance
AWS License Manager,Track, manage, and control licenses,Management & Governance
AWS Config,Track resources inventory and changes,Management & Governance
AWS Systems Manager,Gain operational insights and take action,Management & Governance
AWS Panorama,Improve your operations with computer vision at the edge,Machine Learning
Amazon Kendra,Reinvent enterprise search with ML,Machine Learning
Amazon Forecast,Increase forecast accuracy using machine learning,Machine Learning
Amazon CodeGuru,Find your most expensive lines of code,Machine Learning
AWS Inferentia,Machine learning inference chip,Machine Learning
AWS DeepLens,Deep learning enabled video camera,Machine Learning
Amazon Transcribe,Automatic speech recognition,Machine Learning
Apache MXNet on AWS,Scalable, open-source deep learning framework,Machine Learning
AWS Deep Learning AMIs,Deep learning on Amazon EC2,Machine Learning
Amazon Translate,Natural and fluent language translation,Machine Learning
Amazon Elastic Inference,Deep learning inference acceleration,Machine Learning
Amazon Augmented AI,Easily implement human review of ML predictions,Machine Learning
Amazon Lookout for Equipment,Detect abnormal equipment behavior by analyzing sensor data,Machine Learning
PyTorch on AWS,Flexible open-source machine learning framework,Machine Learning
AWS DeepRacer,Autonomous 1/18th scale race car, driven by ML,Machine Learning
AWS IoT 1-Click,One click creation of an AWS Lambda trigger,Internet Of Things
AWS IoT SiteWise,IoT data collector and interpreter,Machine Learning
Amazon Monitron,Reduce unplanned equipment downtime with predictive maintenance and machine learning,Machine Learning
TensorFlow on AWS,Open-source machine intelligence library,Machine Learning
Amazon Lookout for Metrics,Automatically detect anomalies in metrics and identify their root cause,Machine Learning
Amazon DevOps Guru,ML-powered cloud operations service to improve application availability,Machine Learning
Amazon SageMaker,Build, train, and deploy machine learning models at scale,Machine Learning
Amazon Lex,Build voice and text chatbots,Machine Learning
AWS DeepComposer,ML enabled musical keyboard,Machine Learning
Amazon Textract,Extract text and data from documents,Machine Learning
Amazon HealthLake,Securely store, transform, query, and analyze health data in minutes,Machine Learning
AWS Deep Learning Containers,Docker images for deep learning,Machine Learning
Amazon Personalize,Build real-time recommendations into your applications,Machine Learning
Amazon Lookout for Vision,Spot product defects using computer vision to automate quality inspection,Machine Learning
Amazon Fraud Detector,Detect more online fraud faster,Machine Learning
Amazon Lumberyard,A free cross-platform 3D game engine, with Full Source, integrated with AWS and Twitch,Game Tech
Amazon GameLift,Simple, fast, cost-effective dedicated game server hosting,Internet Of Things
AWS Partner Device Catalog,Curated catalog of AWS-compatible IoT hardware,Internet Of Things
AWS IoT Analytics,Analytics for IoT devices,Internet Of Things
AWS IoT Greengrass,Local compute, messaging, and sync for devices,Internet Of Things
AWS IoT FleetWise,Easily collect, transform, and transfer vehicle data to the cloud in near-real time,Internet Of Things
AWS IoT TwinMaker,Optimize operations by easily creating digital twins of real-world systems,Internet Of Things
FreeRTOS,Real-time operating system for microcontrollers,Internet Of Things
AWS IoT Device Management,Onboard, organize, and remotely manage IoT devices,Internet Of Things
AWS IoT EduKit,Learn how to build simple IoT applications with reference hardware and step-by-step tutorials,Internet Of Things
AWS IoT Button,Cloud programmable dash button,Internet Of Things
AWS IoT RoboRunner,Build applications that help fleets of robots work together seamlessly,Internet Of Things
AWS IoT Core,Connect devices to the cloud,Internet Of Things
AWS IoT Events,IoT event detection and response,Internet Of Things
AWS CodeArtifact,Secure, scalable, and cost-effective artifact management for software development,Developer Tools
AWS CodePipeline,Release software using continuous delivery,Developer Tools
Amazon Corretto,Production-ready distribution of OpenJDK,Developer Tools
AWS X-Ray,Analyze and debug your applications,Developer Tools
AWS CloudShell,Command line access to AWS resources and tools directly from a browser,Developer Tools
AWS Fault Injection Simulator,Improve resiliency and performance with controlled experiments,End User Computing
Amazon WorkSpaces,Virtual desktops in the cloud,End User Computing
Amazon AppStream 2.0,Stream desktop applications securely to a browser,Front-End Web & Mobile
AWS AppSync,Accelerate app development with fully-managed, scalable GraphQL APIs,Front-End Web & Mobile
Amazon Simple Email Service (SES),High-scale inbound and outbound email,Front-End Web & Mobile
Amazon API Gateway,Build, deploy, and manage APIs,Front-End Web & Mobile
AWS Device Farm,Test Android, iOS, and web apps on real devices in the AWS cloud,Front-End Web & Mobile
Amazon Pinpoint,Multichannel marketing communications,Front-End Web & Mobile
Amazon Location Service,Securely and easily add location data to applications,Front-End Web & Mobile
AWS Amplify,Build, deploy, host, and manage scalable web and mobile apps,Game Tech
AWS Cloud Development Kit (CDK),Model cloud infrastructure using code,Developer Tools
AWS Cloud9,Write, run, and debug code on a cloud IDE,Developer Tools
AWS Command Line Interface (CLI),Line Interface Unified tool to manage AWS services,Developer Tools
AWS Tools and SDKs,Tools and SDKs for AWS,Developer Tools
AWS CodeStar,Develop and deploy AWS applications,Developer Tools
AWS CodeBuild,Build and test code,Developer Tools
AWS Cloud Control API,Manage AWS and third-party cloud infrastructure with consistent APIs,Developer Tools
AWS CodeCommit,Store code in private Git repositories,Compute
AWS Wavelength,Deliver ultra-low latency applications for 5G devices,Compute
AWS Auto Scaling,Scale multiple resources to meet demand,Compute
AWS Outposts,Run AWS infrastructure on-premises,Compute
Amazon Lightsail,Launch and manage virtual private servers,Containers
AWS Fargate,Serverless compute for containers,Containers
Amazon Elastic Kubernetes Service (EKS),The most trusted way to run Kubernetes,Containers
Red Hat OpenShift Service on AWS,Managed OpenShift in the cloud,Containers
AWS App2Container,Containerize and migrate existing applications,Containers
Amazon Elastic Container Registry (ECR),Easily store, manage, and deploy container images,Containers
AWS Copilot,AWS Copilot is the easiest way to launch and manage your containerized application on AWS,Containers
Amazon Elastic Container Service (ECS),Highly secure, reliable, and scalable way to run containers,Databases
Amazon Timestream,Fully managed time series database,Databases
Amazon DynamoDB,Managed NoSQL database,Databases
Amazon DocumentDB,Fully managed document database,Databases
Amazon RDS,Managed relational database service for MySQL, PostgreSQL, Oracle, SQL Server, and MariaDB,Databases
Savings Plans,Save up to 72% on compute usage with flexible pricing,Cloud Financial Management
Reserved Instance (RI) Reporting,Dive deeper into your reserved instances (RIs),Cloud Financial Management
AWS Cost and Usage Report,Access comprehensive cost and usage information,Cloud Financial Management
AWS Cost Explorer,Analyze your AWS cost and usage,Cloud Financial Management
AWS Budgets,Set custom cost and usage budgets,Cloud Financial Management
AWS Compute Optimizer,Identify optimal AWS Compute resources,Compute
AWS App Runner,Production web applications at scale made easy for developers,Compute
VMware Cloud on AWS,Build a hybrid cloud without custom hardware,Compute
AWS Serverless Application Repository,Discover, deploy, and publish serverless applications,Compute
AWS Elastic Beanstalk,Run and manage web apps,Compute
AWS Lambda,Run code without thinking about servers,Compute
AWS Batch,Run batch jobs at any scale,Compute
Amazon EC2,Virtual servers in the cloud,Compute
Amazon EC2 Spot Instances,Run workloads for up to 90% off,Compute
Amazon Simple Notification Service (SNS),Pub/sub, SMS, email, and mobile push notifications,Application Integration
Amazon AppFlow,No-code integration for SaaS apps & AWS services,Application Integration
Amazon Simple Queue Service (SQS),Managed message queues,Application Integration
AWS Step Functions,Coordination for distributed applications,Application Integration
Amazon MQ,Managed message broker service,Architecture Strategy
AWS Well-Architected Tool,Review and improve your workloads,Blockchain
Amazon Managed Blockchain,Create and manage scalable blockchain networks,Blockchain
Amazon Quantum Ledger Database (QLDB),Fully managed ledger database,Business Applications
Amazon WorkMail,Secure email and calendaring,Business Applications
Amazon WorkDocs,Secure enterprise document storage and sharing,Business Applications
Alexa for Business,Empower your organization with Alexa,Business Applications
Amazon Connect,Omnichannel cloud contact center,Business Applications
Amazon Honeycode,Build mobile & web apps without programming,Business Applications
Amazon Chime,Frustration-free meetings, video calls, and chat,Business Applications
Amazon Chime SDK,Real-time messaging, audio, video, and screen sharing,Business Applications
Amazon Sumerian,Build and run AR and VR applications,AR & VR
AWS Glue,Simple, scalable, and serverless data integration,Analytics
Amazon Athena,Query data in S3 using SQL,Analytics
Amazon OpenSearch Service (successor to Amazon Elasticsearch Service),Search, visualize, and analyze up to petabytes of text and unstructured data,Analytics
AWS Data Pipeline,Orchestration service for periodic, data-driven workflows,Analytics
Amazon FinSpace,Store, catalog, prepare, and analyze financial industry data in minutes,Analytics
AWS Lake Formation,Build a secure data lake in days,Analytics
Amazon EMR,Hosted Hadoop framework,Analytics
Amazon CloudSearch,Managed search service,Analytics
Amazon Kinesis,Analyze real-time video and data streams,Analytics
AWS Data Exchange,Find, subscribe to, and use third-party data in the cloud,Analytics
Amazon QuickSight,Fast business analytics service,Analytics
Amazon Managed Streaming for Apache Kafka (MSK),Fully managed Apache Kafka service,Application Integration
Amazon Managed Workflows for Apache Airflow (MWAA),Highly available, secure, and managed workflow orchestration for Apache Airflow,Application Integration
Amazon EventBridge,Serverless event bus for SaaS apps & AWS services