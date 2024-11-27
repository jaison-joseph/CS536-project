package nsfnet;

import inet.node.inet.StandardHost;
import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.node.ethernet.Eth100M;  // Changed this import
import inet.common.scenario.ScenarioManager;

network NSFNetwork
{
    parameters:
        @display("bgb=800,600");
    
    submodules:
        configurator: Ipv4NetworkConfigurator {
            @display("p=100,100");
            config = xml("<config><interface hosts='*' address='10.0.0.x' netmask='255.255.255.0'/></config>");  // Added IP configuration
        }
        scenarioManager: ScenarioManager {
            @display("p=100,200;is=s");
        }
        
        n0: StandardHost {
            @display("p=200,100");
        }
        n1: StandardHost {
            @display("p=200,300");
        }
        n2: StandardHost {
            @display("p=400,200");
            forwarding = true;  // Enable forwarding for n2
        }
        
    connections:
        n0.ethg++ <--> Eth100M <--> n2.ethg++;  // Changed to ethernet
        n1.ethg++ <--> Eth100M <--> n2.ethg++;  // Changed to ethernet
}