# -*- coding: utf-8 -*-

"""Migration to create a Dataverse Transfer Type."""

from __future__ import unicode_literals

import logging

from django.db import migrations

# Can't use apps.get_model for this model as we need to access class attributes.
from main.models import Job

# Get an instance of a logger
logger = logging.getLogger(__name__)
logger.setLevel("INFO")

DEFAULT_NEXT_MS = "61c316a6-0a50-4f65-8767-1f44b1eeb6dd"


def update_task(apps, schema_editor, task_uuid, task_config):
    """Update the task config table when we have all the info needed."""
    tasks_config_table = apps.get_model('main', 'TaskConfig')
    tasks_config_table.objects.filter(
        id=task_uuid
    ).update(tasktypepkreference=task_config)


def create_ms_dict_choice(
        apps, schema_editor,
        choice_uuid, desc, replacement_dict, link_uuid):
    """Create a dictionary based choice in the database."""
    microservice_dict_choice_table = apps\
        .get_model('main', 'MicroServiceChoiceReplacementDic')
    microservice_dict_choice_table.objects.create(
        id=choice_uuid,
        description=desc,
        choiceavailableatlink=get_ms_chain_link_instance(
            apps,
            schema_editor,
            ms_uuid=link_uuid
        ),
        replacementdic=replacement_dict,
    )


# Functions to help return ORM object instances for various MS entries.
def get_ms_chain_instance(apps, schema_editor, chain_uuid):
    """Return an object instance of a Microservice Chain to the calling
    function.
    """
    return apps\
        .get_model("main", "MicroServiceChain")\
        .objects.get(id=chain_uuid)


def get_ms_chain_link_instance(apps, schema_editor, ms_uuid):
    """Get chainlink instance from the database."""
    return apps\
        .get_model("main", "MicroServiceChainLink")\
        .objects.get(id=ms_uuid)


def get_task_type_instance(apps, schema_editor, task_type_uuid):
    """Get a task type instance from the database."""
    return apps\
        .get_model('main', 'TaskType')\
        .objects.get(id=task_type_uuid)


def get_watched_type_instance(apps, schema_editor, type_uuid):
    """Return a watched directory type from the database."""
    return apps\
        .get_model('main', 'WatchedDirectoryExpectedType')\
        .objects.get(id=type_uuid)


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------


def create_variable_link_pull(
        apps, link_uuid, variable, ms_uuid):
    """Create a new variable link pull in the database."""
    apps.get_model("main", "TaskConfigUnitVariableLinkPull").objects.create(
        id=link_uuid,
        variable=variable,
        defaultmicroservicechainlink_id=ms_uuid,
    )


def create_set_unit_variable(
        apps, var_uuid, variable_name, variable_value=None, ms_uuid=None):
    """Create a new unit variable in the database."""
    apps.get_model("main", "TaskConfigSetUnitVariable").objects.create(
        id=var_uuid,
        variable=variable_name,
        variablevalue=variable_value,
        microservicechainlink_id=ms_uuid,
    )


def create_standard_task_config(apps, task_uuid, execute_string, args):
    """Create a task configuration, inc. the command and args and write to the
    database.
    """
    get_model(apps, "StandardTaskConfig").objects.create(
        id=task_uuid, execute=execute_string, arguments=args,
    )


def create_task(
        apps, task_type_uuid, task_uuid, task_desc, task_config=None):
    """Create a new task configuration entry in the database."""
    get_model(apps, 'TaskConfig').objects.create(
        id=task_uuid, description=task_desc, tasktype_id=task_type_uuid,
        tasktypepkreference=task_config,
    )


def create_ms_chain_link(
        apps, ms_uuid, group, task_uuid, ms_exit_message=Job.STATUS_FAILED,
        default_next_link=DEFAULT_NEXT_MS):
    """Create a microservice chainlink in the database."""
    apps.get_model("main", "MicroServiceChainLink").objects.create(
        id=ms_uuid,
        microservicegroup=group,
        defaultexitmessage=ms_exit_message,
        currenttask_id=task_uuid,
        defaultnextchainlink_id=default_next_link,
    )


def create_ms_chain(apps, chain_uuid, ms_uuid, chain_description):
    """Create a new chain in the database."""
    apps.get_model("main", "MicroServiceChain").objects.create(
        id=chain_uuid,
        startinglink_id=ms_uuid,
        description=chain_description,
    )


def create_ms_choice(apps, choice_uuid, chain_uuid, link_uuid):
    """Create a choice in the database."""
    apps.get_model('main', 'MicroServiceChainChoice').objects.create(
        id=choice_uuid,
        chainavailable_id=chain_uuid,
        choiceavailableatlink_id=link_uuid,
    )


def create_watched_dir(
        apps, watched_uuid, dir_path, expected_type, chain_uuid):
    """Create a new watched directory in the database."""
    get_model(apps, "WatchedDirectory").objects.create(
        id=watched_uuid, watched_directory_path=dir_path,
        expected_type_id=expected_type, chain_id=chain_uuid,
    )


def create_ms_exit_codes(
        apps, exit_code_uuid, ms_in, ms_out,
        ms_exit_message=Job.STATUS_COMPLETED_SUCCESSFULLY):
    """Create an exit code entry in the database."""
    apps.get_model("main", "MicroServiceChainLinkExitCode").objects.create(
        id=exit_code_uuid,
        microservicechainlink_id=ms_in,
        nextmicroservicechainlink_id=ms_out,
        exitmessage=ms_exit_message,
    )


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------


def create_units(apps):

    #def create_variable_link_pull(
    #    apps, link_uuid, variable, ms_uuid):
    #def create_set_unit_variable(
    #    apps, var_uuid, variable_name, variable_value=None, ms_uuid=None):

    create_task(
        apps=apps, task_type_uuid="6f0b612c-867f-4dfd-8e43-5b35b7f882d7",
        task_uuid="2b2042d4-548f-4c63-a394-bf14b5faa5d1",
        task_desc="Send Transfer via Dataverse METS conversion",
        tasktypepkreference="f5908626-38be-4c2b-9c09-a389585e9f6c")

    create_ms_chain_link(
        apps=apps, ms_uuid="213fe743-f170-4695-8b3e-77886a31a89d",
        group="Verify transfer compliance",
        task_uuid="2b2042d4-548f-4c63-a394-bf14b5faa5d1")

    create_set_unit_variable(
        apps=apps, var_uuid="f5908626-38be-4c2b-9c09-a389585e9f6c",
        variable_name="linkToConvertDataverseStructure",
        variable_value="Transfers.type = 'Dataverse'",
        ms_uuid="213fe743-f170-4695-8b3e-77886a31a89d")

    #create_variable_link_pull(
    #    apps=apps, link_uuid="5b11c0a9-6f62-4d7e-ad48-2905e75ff419",
    #    variable="linkToConvertDataverseStructure", ms_uuid=DEFAULT_NEXT_MS)


def data_migration_up(apps, schema_editor):

    create_standard_task_config(
        apps=apps, task_uuid="ed3cda67-94b6-457e-9d00-c58f413dbfce",
        execute_string="archivematicaSetTransferType_v0.0",
        args="\"%SIPUUID%\" \"Dataverse\"")

    create_task(
        apps=apps, task_type_uuid="61fb3874-8ef6-49d3-8a2d-3cb66e86a30c",
        task_uuid="477bc37e-b6a7-440a-9088-85672b3b38a7",
        task_desc="Approve Dataverse Transfer")

    create_task(
        apps=apps, task_type_uuid="36b2e239-4a57-4aa5-8ebc-7a29139baca6",
        task_uuid="4d36c35a-0829-4b2d-ba3d-0a30a3e837f9",
        task_desc="Set transfer type: Dataverse",
        task_config="ed3cda67-94b6-457e-9d00-c58f413dbfce"
    )

    # create ms
    create_ms_chain_link(
        apps=apps, ms_uuid="246943e4-d203-48e1-ac84-4865520e7c30",
        group="Approve Dataverse transfer",
        task_uuid="477bc37e-b6a7-440a-9088-85672b3b38a7")

    # move to processing dir
    create_ms_chain_link(
        apps=apps, ms_uuid="fdb12ea6-22aa-46c8-a591-a2bcf5d42e5e",
        group="Verify transfer compliance",
        task_uuid="7c02a87b-7113-4851-97cd-2cf9d3fc0010")

    # set transfer type: dataverse
    create_ms_chain_link(
        apps=apps, ms_uuid="0af6b163-5455-4a76-978b-e35cc9ee445f",
        group="Verify transfer compliance",
        task_uuid="4d36c35a-0829-4b2d-ba3d-0a30a3e837f9")

    # create chain
    create_ms_chain(
        apps=apps, chain_uuid="35a26b59-dcf3-45ec-b963-ba7bfaa8304f",
        ms_uuid="246943e4-d203-48e1-ac84-4865520e7c30",
        chain_description="Dataverse Transfers in Progress")

    create_ms_chain(
        apps=apps, chain_uuid="10c00bc8-8fc2-419f-b593-cf5518695186",
        ms_uuid="fdb12ea6-22aa-46c8-a591-a2bcf5d42e5e",
        chain_description="Approve Dataverse transfer")

    # Approve
    create_ms_choice(
        apps=apps, choice_uuid="dc9b59b3-dd5f-4cd6-8e97-ee1d83734c4c",
        chain_uuid="10c00bc8-8fc2-419f-b593-cf5518695186",
        link_uuid="246943e4-d203-48e1-ac84-4865520e7c30")

    # Reject
    create_ms_choice(
        apps=apps, choice_uuid="77bb4993-9f5b-4e60-bbe9-0039a6f5934e",
        chain_uuid="1b04ec43-055c-43b7-9543-bd03c6a778ba",
        link_uuid="246943e4-d203-48e1-ac84-4865520e7c30")

    create_watched_dir(
        apps=apps, watched_uuid="3901db52-dd1d-4b44-9d86-4285ddc5c022",
        dir_path="%watchDirectoryPath%activeTransfers/dataverseTransfer",
        expected_type="f9a3a93b-f184-4048-8072-115ffac06b5d",
        chain_uuid="35a26b59-dcf3-45ec-b963-ba7bfaa8304f")

    # TODO look up these tasks and then annotate what they are...
    create_ms_exit_codes(
        apps=apps, exit_code_uuid="f7e3753c-4df9-43fe-9c32-0d11c511308c",
        ms_in="fdb12ea6-22aa-46c8-a591-a2bcf5d42e5e",
        ms_out="0af6b163-5455-4a76-978b-e35cc9ee445f")

    create_ms_exit_codes(
        apps=apps, exit_code_uuid="da46e870-290b-4fd4-8f84-194b9177d8c0",
        ms_in="0af6b163-5455-4a76-978b-e35cc9ee445f",
        ms_out="50b67418-cb8d-434d-acc9-4a8324e7fdd2")

    # TODO start to split these things up ...
    create_units(apps)

def get_model(apps, model_name):
    return apps.get_model("main", model_name)


def data_migration_down(apps, schema_editor):
    get_model(apps=apps, model_name="StandardTaskConfig").objects.filter(
        id="ed3cda67-94b6-457e-9d00-c58f413dbfce").delete()
    get_model(apps, 'TaskConfig').objects.filter(
        id="477bc37e-b6a7-440a-9088-85672b3b38a7").delete()
    get_model(apps, 'TaskConfig').objects.filter(
        id="4d36c35a-0829-4b2d-ba3d-0a30a3e837f9").delete()
    get_model(apps, 'MicroServiceChainLink').objects.filter(
        id="246943e4-d203-48e1-ac84-4865520e7c30").delete()
    get_model(apps, 'MicroServiceChainLink').objects.filter(
        id="fdb12ea6-22aa-46c8-a591-a2bcf5d42e5e").delete()
    get_model(apps, 'MicroServiceChainLink').objects.filter(
        id="0af6b163-5455-4a76-978b-e35cc9ee445f").delete()
    get_model(apps, 'MicroServiceChain').objects.filter(
        id="10c00bc8-8fc2-419f-b593-cf5518695186").delete()
    get_model(apps, 'MicroServiceChain').objects.filter(
        id="35a26b59-dcf3-45ec-b963-ba7bfaa8304f").delete()
    get_model(apps, 'MicroServiceChainChoice').objects.filter(
        id="dc9b59b3-dd5f-4cd6-8e97-ee1d83734c4c").delete()
    get_model(apps, 'MicroServiceChainChoice').objects.filter(
        id="77bb4993-9f5b-4e60-bbe9-0039a6f5934e").delete()
    get_model(apps=apps, model_name="WatchedDirectory").objects.filter(
        id="3901db52-dd1d-4b44-9d86-4285ddc5c022").delete()
    get_model(apps=apps, model_name="MicroServiceChainLinkExitCode")\
        .objects.filter(id="f7e3753c-4df9-43fe-9c32-0d11c511308c").delete()
    get_model(apps=apps, model_name="MicroServiceChainLinkExitCode")\
        .objects.filter(id="da46e870-290b-4fd4-8f84-194b9177d8c0").delete()

    # convert dataverse structure...
    get_model(apps, 'TaskConfig').objects.filter(
        id="2b2042d4-548f-4c63-a394-bf14b5faa5d1").delete()
    get_model(apps, 'MicroServiceChainLink').objects.filter(
        id="213fe743-f170-4695-8b3e-77886a31a89d").delete()
    get_model(apps, 'TaskConfigSetUnitVariable').objects.filter(
        id="f5908626-38be-4c2b-9c09-a389585e9f6c").delete()



class Migration(migrations.Migration):

    dependencies = [
        ('main', '0058_fix_unit_variable_pull_link'),
    ]

    operations = [
        migrations.RunPython(data_migration_up, data_migration_down),
    ]
