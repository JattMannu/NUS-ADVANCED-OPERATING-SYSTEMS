'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
'''
import sys
import copy
import queue 
input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrival_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

    def __lt__(self, other):
        return self.burst_time < other.burst_time

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum ):
    time = 0
    finishedQ = queue.Queue()
    runnableQ = queue.Queue()
    #Assume 1 epoch.
    current_process = None

    current_time_quantum = 0;
    for tick in range(0, 0):
        
        print(tick)
        
        for task in process_list:
            if task.arrive_time == tick:   
                runnableQ.put(task)

        if current_time_quantum == 0:
            if current_process != None and current_process.burst_time > 0:
                runnableQ.put(current_process)
            elif current_process != None:
                print("\t FINISHED " + current_process.__repr__())
                finishedQ.put(current_process)
            #else:
                #print("\t CPU IDLE")

            if(not runnableQ.empty()):
                current_process = runnableQ.get_nowait()
                current_time_quantum = time_quantum #Give the new process some time slice.
            else:
                current_process = None


        else:
            #current_time_quantum is not 0 and the current_process is finished
            if current_process != None and current_process.burst_time == 0:
                finishedQ.put(current_process)
                current_time_quantum = 0
                print("\t FINISHED " + current_process.__repr__())
                if(not runnableQ.empty()):
                    current_process = runnableQ.get_nowait()
                    current_time_quantum = time_quantum
                else:
                    current_process = None
        
        
        if current_process != None:
            current_process.burst_time -= 1
            current_time_quantum  -= 1  
            print("\t CPU = " + current_process.__repr__() + "\tRunableQ is "+ str(runnableQ.qsize())+ "\tcurrent_time_quantum: "+str(current_time_quantum))
        else:    
            print("\t CPU IDLE\tRunableQ size: "+ str(runnableQ.qsize()) + "\tcurrent_time_quantum: "+str(current_time_quantum))
        
    #print(runnableQ.qsize())
    #print(finishedQ.qsize())
    return (["to be completed, scheduling process_list on round robin policy with time_quantum"], 0.0)

def SRTF_scheduling(process_list):
    time = 0
    finishedQ = queue.Queue()
    runnableQ = queue.PriorityQueue()
    
    current_process = None
    for tick in range(-1, 200):
        print(tick)
        for task in process_list:
            if task.arrive_time == tick:   
                #print("\t task added to runnableQ= " + task.__repr__())
                runnableQ.put(task)

        if (not runnableQ.empty()):
            current_process = runnableQ.get_nowait();

        if current_process != None:
            current_process.burst_time -= 1
            print("\t CPU = " + current_process.__repr__() + "\tRunableQ is "+ str(runnableQ.qsize()))
            if current_process.burst_time  == 0:
                finishedQ.put(current_process)
                print("\t FINISHED ")
            else:
                runnableQ.put(current_process)
            current_process = None
        else:    
            print("\t CPU IDLE\tRunableQ size: "+ str(runnableQ.qsize()))

    return (["to be completed, scheduling process_list on SRTF, using process.burst_time to calculate the remaining time of the current process "], 0.0)

def SJF_scheduling(process_list, alpha):
    finishedQ = []
    runnableQ = copy.deepcopy(process_list)
    return (["to be completed, scheduling SJF without using information from process.burst_time"],0.0)


def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])

