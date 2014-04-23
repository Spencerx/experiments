
import os
from config.experiment_config_lib import ControllerConfig
from sts.topology import MeshTopology
from sts.control_flow import Fuzzer, Interactive
from sts.input_traces.input_logger import InputLogger
from sts.simulation_state import SimulationConfig
from sts.util.convenience import timestamp_string, find, backtick, system

vagrant_dir = "/mnt/ahassany/vagrant_onosdev"
onos_dir = "ONOS"

if 'CLUSTER' not in os.environ:
  raise RuntimeError('''Need to set $CLUSTER. See '''
                     '''https://wiki.onlab.us:8443/display/Eng/ONOS+Development+VM.\n'''
                     '''On c5:\n'''
                     '''export CLUSTER=${HOME}/.cluster.hosts\n'''
                     '''export ONOS_CLUSTER_BASENAME="onosdev"\n'''
                     '''export ONOS_CLUSTER_NR_NODES=2\n'''
                     '''export PATH=${HOME}/vagrant_onosdev/ONOS/cluster-mgmt/bin:$PATH''')

def get_additional_metadata():
  path = vagrant_dir + "/" + onos_dir
  return {
    'commit' : backtick("git rev-parse HEAD", cwd=path),
    'branch' : backtick("git rev-parse --abbrev-ref HEAD", cwd=path)
  }

# Use ONOS as our controller.
# TODO(cs): first make sure to clean up any preexisting ONOS instances.
# N.B. this command is for the entire cluster, not individual nodes.
"""
start_cmd = (''' vagrant halt onosdev1 onosdev2; vagrant up onosdev1 onosdev2 ; '''
             ''' ./scripts/conf_setup.sh 2 ; zk start ; cassandra start; '''
             ''' onos start ; sleep 30 ''')
"""

start_cmd = (#''' vagrant halt onosdev1 onosdev2 onosdev3 onosdev4; vagrant up onosdev1 onosdev2 onosdev3 onodev4 ; '''
             ''' onos stop; zk stop ; cassandra stop; echo "sleeping for 5sec"; sleep 5;'''
             ''' %s/scripts/conf_setup.sh 2 ; zk start ; cassandra start; echo "sleeping for 10sec"; sleep 10 ;'''
             ''' onos start ; echo "sleeping for 40 secs"; sleep 40 ;'''
             ''' onos stop; sleep 10; cassandra cleandb; onos start; sleep 40'''% (vagrant_dir)
            )

print "START COMMAND", start_cmd

"""
# N.B kills a single node.
kill_cmd = (''' vagrant ssh %s -c "cd ONOS; ./start-onos.sh stop"''')
# N.B. starts a single node.
restart_cmd = 'vagrant ssh %s -c "cd ONOS; ./start-onos.sh start"'
dummy_cmd = 'sleep 1'
"""

# N.B kills a single node.
kill_cmd = (''' ssh %s "cd %s; ./start-onos.sh stop"; echo "killed"; sleep 5''')
# N.B. starts a single node.
restart_cmd = 'ssh %s "cd %s; ./start-onos.sh start"; echo "restarted"; sleep 20'
dummy_cmd = 'echo "DUMMY COMMAND"; sleep 1'

"""
controllers = [ControllerConfig(start_cmd, address="192.168.56.11", port=6633,
                                kill_cmd=kill_cmd % "onosdev1",
                                restart_cmd=restart_cmd % "onosdev1",
                                controller_type="onos",
                                cwd="/home/rcs/vagrant_onosdev"),
               ControllerConfig(dummy_cmd, address="192.168.56.12", port=6633,
                                kill_cmd=kill_cmd % "onosdev2",
                                restart_cmd=restart_cmd % "onosdev2",
                                controller_type="onos",
                                cwd="/home/rcs/vagrant_onosdev")]
"""
controllers = [ControllerConfig(start_cmd, address="192.168.56.11", port=6633,
                                kill_cmd=kill_cmd % ("onosdev1", onos_dir),
                                restart_cmd=restart_cmd % ("onosdev1", onos_dir),
                                controller_type="onos",
                                cwd=vagrant_dir),
               ControllerConfig(dummy_cmd, address="192.168.56.12", port=6633,
                                kill_cmd=kill_cmd % ("onosdev2", onos_dir),
                                restart_cmd=restart_cmd % ("onosdev2", onos_dir),
                                controller_type="onos",
                                cwd=vagrant_dir), ]
'''
               ControllerConfig(dummy_cmd, address="192.168.56.13", port=6633,
                                kill_cmd=kill_cmd % ("onosdev3", onos_dir),
                                restart_cmd=restart_cmd % ("onosdev3", onos_dir),
                                controller_type="onos",
                                cwd=vagrant_dir),
               ControllerConfig(dummy_cmd, address="192.168.56.14", port=6633,
                                kill_cmd=kill_cmd % ("onosdev4", onos_dir),
                                restart_cmd=restart_cmd % ("onosdev4", onos_dir),
                                controller_type="onos",
                                cwd=vagrant_dir),]
'''

topology_class = MeshTopology
topology_params = "num_switches=2" # ",netns_hosts=True"

simulation_config = SimulationConfig(controller_configs=controllers,
                                     topology_class=topology_class,
                                     topology_params=topology_params,
                                     #violation_persistence_threshold=1,
                                     kill_controllers_on_exit=False)

#control_flow = Fuzzer(simulation_config, check_interval=20,
#                      halt_on_violation=True,
#                      input_logger=InputLogger(),
#                      invariant_check_name="InvariantChecker.check_loops")


control_flow = Fuzzer(simulation_config, check_interval=40,
                      halt_on_violation=True,
                      input_logger=InputLogger(),
                      #steps=100,
                      invariant_check_name="InvariantChecker.check_liveness")
                      #invariant_check_name="check_for_flow_entry")
                      #invariant_check_name="InvariantChecker.check_connectivity")
                      #invariant_check_name="check_everything")

#control_flow = Interactive(simulation_config, input_logger=InputLogger())

raise RuntimeError("Please add this parameter to Fuzzer: fuzzer_params='experiments/distributed_onos_2014_01_31_00_42_51/fuzzer_params.py'")