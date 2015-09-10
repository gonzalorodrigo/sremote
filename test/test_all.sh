#!/bin/bash

 python -m unittest test_tools

 python -m unittest test_newt_connector.TestNewt
 python -m unittest test_ssh_connector.TestSsh
 
 python -m unittest test_server_channel
 
 python -m unittest test_remote_client_newt.TestRemoteClientNEWT
 python -m unittest test_remote_client_ssh.TestRemoteClientSSH




