import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, Bool

class Intermediary_Arm(Node):
    def __init__(self):
        super().__init__('arm_intermediary')
        self.publisher_joint1 = self.create_publisher(Float64, 'maxon/canopen_motor/base_link1_joint_position_controller/command',10 )
        self.publisher_joint2 = self.create_publisher(Float64, 'maxon/canopen_motor/base_link2_joint_position_controller/command',10 )
        
        self.subscriber_joint1 = self.create_subscription(Float64, 'arm_teleop/joint1',self.callbackjoint1,10)
        self.subscriber_joint2 = self.create_subscription(Float64, 'arm_teleop/joint2',self.callbackjoint2,10)
        
        self.subscriber_emergency = self.create_subscription(Bool,'arm_teleop/emergency',self.callbackemergency,10)
        
        self.iniciojoint1=0
        self.iniciojoint2=0
        self.emergency = False
        
        self.regla3joint1=425984/360
        self.regla3joint2=1990656/360
        
    
    def operation_joint1(self,data):
        return (data*self.regla3joint1)-(self.iniciojoint1*self.regla3joint1)
    
    def callbackjoint1(self,data):
        in1=float(data.data)
        datos=Float64()
        datos.data=self.operation_joint1(in1)      
        self.publisher_joint1.publish(datos)
        
    def operation_joint2(self,data):
        return (data*self.regla3joint2)-(self.iniciojoint2*self.regla3joint2)
    
    def callbackjoint2(self,data):
        in2=float(data.data)
        datos=Float64()
        datos.data=self.operation_joint1(in2)
        self.publisher_joint2.publish(datos)
        
    def callbackemergency(self,data):
        self.emergency=data.data
        if self.emergency:
            print("Ingresa la posicion actual del joint 1")
            self.iniciojoint1=float(input())
            print("Ingresa la posicion actual del joint 2")
            self.iniciojoint2=float(input())
    
    def main(self):
        print("hola")
    
def main(args=None):
    rclpy.init(args=args)
    intermediary=Intermediary_Arm()
    rclpy.spin(intermediary)
    intermediary.destroy_node()
    rclpy.shutdown()
    
if __name__ =='__name__':
    main()