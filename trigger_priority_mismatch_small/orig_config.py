
from config.experiment_config_lib import ControllerConfig
from sts.topology import MeshTopology, FatTree
from sts.control_flow import Fuzzer
from sts.input_traces.input_logger import InputLogger
from sts.simulation_state import SimulationConfig

# Use POX as our controller
start_cmd = ('''./pox.py --verbose '''
             #'''sts.syncproto.pox_syncer --blocking=False '''
             '''openflow.discovery forwarding.l2_multi '''
             '''forwarding.capabilities_manager '''
             '''sts.util.socket_mux.pox_monkeypatcher '''
             '''openflow.of_01 --address=__address__ --port=__port__''')

controllers = [ControllerConfig(start_cmd, cwd="pox")]
#topology_class = FatTree
#topology_params = "num_pods=4"
topology_class = MeshTopology
topology_params = "num_switches=2"

simulation_config = SimulationConfig(controller_configs=controllers,
                                     topology_class=topology_class,
                                     topology_params=topology_params,
                                     multiplex_sockets=True)

control_flow = Fuzzer(simulation_config, check_interval=1,
                      fuzzer_params='experiments/trigger_priority_mismatch/fuzzer_params.py',
                      halt_on_violation=True,
                      initialization_rounds=50,
                      send_all_to_all=False,
                      input_logger=InputLogger(),
                      invariant_check_name="check_for_flow_entry")

raise RuntimeError("Please add this parameter to Fuzzer: fuzzer_params='experiments/trigger_priority_mismatch_small/fuzzer_params.py'")