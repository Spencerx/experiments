
from config.experiment_config_lib import ControllerConfig
from sts.topology import *
from sts.control_flow import Replayer
from sts.simulation_state import SimulationConfig
from sts.input_traces.input_logger import InputLogger

simulation_config = SimulationConfig(controller_configs=[ControllerConfig(start_cmd='./pox.py --verbose openflow.discovery forwarding.l2_multi_broken_floyd sts.util.socket_mux.pox_monkeypatcher openflow.of_01 --address=__address__ --port=7777',
    label='c1', address='127.0.0.1', cwd='pox', port=7777)],
                 topology_class=MeshTopology,
                 topology_params="num_switches=4",
                 patch_panel_class=BufferedPatchPanel,
                 multiplex_sockets=True,
                 kill_controllers_on_exit=True)

control_flow = Replayer(simulation_config, "experiments/pox_broken_floyd/events.trace",
                        input_logger=InputLogger(),
                        wait_on_deterministic_values=False,
                        allow_unexpected_messages=False,
                        delay_flow_mods=False,
                        default_dp_permit=True,
                        pass_through_whitelisted_messages=True,
                        invariant_check_name='InvariantChecker.check_loops',
                        bug_signature="")
