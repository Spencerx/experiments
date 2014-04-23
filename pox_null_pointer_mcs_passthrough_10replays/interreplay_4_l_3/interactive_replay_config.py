
from config.experiment_config_lib import ControllerConfig
from sts.topology import *
from sts.control_flow.interactive_replayer import InteractiveReplayer
from sts.simulation_state import SimulationConfig
from sts.input_traces.input_logger import InputLogger

simulation_config = SimulationConfig(controller_configs=[ControllerConfig(start_cmd='./pox.py --verbose openflow.discovery forwarding.l2_multi_null_pointer sts.util.socket_mux.pox_monkeypatcher openflow.of_01 --address=../sts_socket_pipe', label='c1', address='sts_socket_pipe', cwd='pox')],
                 topology_class=FatTree,
                 topology_params="",
                 patch_panel_class=BufferedPatchPanel,
                 multiplex_sockets=True,
                 kill_controllers_on_exit=True)

control_flow = InteractiveReplayer(simulation_config, "experiments/pox_null_pointer_mcs_passthrough_10replays/interreplay_4_l_3/events.trace")
# wait_on_deterministic_values=False
# delay_flow_mods=False
# Invariant check: 'InvariantChecker.check_liveness'
# Bug signature: "c1"
