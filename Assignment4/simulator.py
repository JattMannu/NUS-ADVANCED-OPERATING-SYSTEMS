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
        self.burst_time_bak = burst_time
        self.compare = None
        self.first_call = None
        self.finish_time = None
        self.predicted_burst = None

    def amount_waited(self):
        return self.finish_time - self.arrive_time - self.burst_time_bak

    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrival_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

    def __lt__(self, other):
        #return self.burst_time < other.burst_time
        return self.compare(self, other)

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
    finishedQ = queue.Queue()
    runnableQ = queue.Queue()
    current_process = None
    out_put = []

    current_time_quantum = 0
    for tick in range(-10, 130):
        
        print(tick)
        
        for task in process_list:
            if task.arrive_time == tick:   
                runnableQ.put(task)

        if current_time_quantum == 0:
            if current_process != None and current_process.burst_time > 0:
                runnableQ.put(current_process)
            elif current_process != None:
                current_process.finish_time = tick
                print("\t FINISHED " + current_process.__repr__())
                finishedQ.put(current_process)

            if(not runnableQ.empty()):
                current_process = runnableQ.get_nowait()
                out_put.append((tick, current_process.id))
                current_time_quantum = time_quantum #Give the new process some time slice.
                if current_process.first_call == None:
                    current_process.first_call = tick
            else:
                current_process = None
        else:
            #current_time_quantum is not 0 and the current_process is finished
            if current_process != None and current_process.burst_time == 0:
                current_process.finish_time = tick
                finishedQ.put(current_process)
                current_time_quantum = 0
                current_process = None
                print("\t FINISHED " + current_process.__repr__())
                # if(not runnableQ.empty()):
                #     current_process = runnableQ.get_nowait()
                #     out_put.append((tick, current_process.id))
                #     current_time_quantum = time_quantum
                #     if current_process.first_call == None:
                #         current_process.first_call = tick
                # else:
                #     current_process = None
        
        if current_process != None:
            current_process.burst_time -= 1
            current_time_quantum  -= 1  
            print("\t CPU = " + current_process.__repr__() + "\tRunableQ is "+ str(runnableQ.qsize())+ "\tcurrent_time_quantum: "+str(current_time_quantum))
        else:    
            print("\t CPU IDLE \tRunableQ size: "+ str(runnableQ.qsize()) + "\tcurrent_time_quantum: "+str(current_time_quantum))
        
    #print(runnableQ.qsize())
    #print(finishedQ.qsize())
    total_wait = 0
    for task in process_list:
        #wait =  task.first_call - task.arrive_time 
        print(str(task.id) +" : "+ str(task.amount_waited()))
        total_wait += task.amount_waited()
        print(task.finish_time)
    avg_wait = total_wait / len(process_list)
    print(out_put)
    print(str(avg_wait))

    #return (["to be completed, scheduling process_list on round robin policy with time_quantum"], avg_wait)
    return (out_put, avg_wait)

def SRTF_compare(param1,param2):
    return param1.burst_time < param2.burst_time

def SRTF_scheduling(process_list):
    _process_list = copy.deepcopy(process_list)
    finishedQ = queue.Queue()
    runnableQ = queue.PriorityQueue()
    out_put = []
    prev_id = -1
    current_process = None
    for tick in range(-1, 130):
        print(tick)
        for task in _process_list:
            if task.arrive_time == tick:   
                task.compare = SRTF_compare 
                runnableQ.put(task)


        if (not runnableQ.empty()):
            current_process = runnableQ.get_nowait()
            if prev_id != current_process.id:
                out_put.append((tick, current_process.id))
            if current_process.first_call != None:
                current_process.first_call = tick


        if current_process != None:
            current_process.burst_time -= 1
            print("\t CPU = " + current_process.__repr__() + "\tRunableQ is "+ str(runnableQ.qsize()))
            if current_process.burst_time  == 0:
                current_process.finish_time = tick
                finishedQ.put(current_process)
                print("\t FINISHED ")
            else:
                runnableQ.put(current_process)
            prev_id = current_process.id
            current_process = None
        else:    
            print("\t CPU IDLE\tRunableQ size: "+ str(runnableQ.qsize()))

    total_wait = 0
    for task in _process_list:
        #wait =  task.first_call - task.arrive_time 
        #print(task.amount_waited())
        total_wait += task.amount_waited() + 1
        #print(task.finish_time)
    avg_wait = total_wait / len(process_list)
    print(out_put)
    print(str(avg_wait))
    return (out_put, avg_wait)

def SJF_compare(param1,param2):
    return param1.predicted_burst < param2.predicted_burst

def predict_bust(a, t_n ,tp_n):
    return a*t_n + (1 - a)* tp_n

def SJF_scheduling(process_list, alpha):
    _process_list = copy.deepcopy(process_list)
    finishedQ = queue.Queue()
    runnableQ = queue.PriorityQueue()
    current_process = None
    out_put = []
    prev_id = -1
    tp_ns = [5 ,5 ,5 ,5]

    for tick in range(-1, 150):
        print(tick)
        for task in _process_list:
            if task.arrive_time == tick:
                  #=   predict_bust(alpha,task.burst_time,tp_ns[task.id])
                task.predicted_burst = tp_ns[task.id]
                tp_ns[task.id] = predict_bust(alpha,task.burst_time,tp_ns[task.id])
                #print("\ttaskid = "+str(task.id)+"\tburst_time_bak = " +str(task.burst_time_bak)+ "\t predicted_burst = " +str(task.predicted_burst))
                #print("\t task added to runnableQ= " + task.__repr__())
                task.compare = SJF_compare 
                runnableQ.put(task)
            
        if current_process != None and current_process.burst_time > 0:
            prev_id = current_process.id
            current_process.burst_time -= 1
            print("\t CPU = " + current_process.__repr__() + "\tRunableQ is "+ str(runnableQ.qsize()))
        elif current_process != None:
            current_process.finish_time = tick
            finishedQ.put(current_process)
            current_process = None
            print("\t FINISHED ")

        if (not runnableQ.empty() and current_process == None):
            current_process = runnableQ.get_nowait()
            out_put.append((tick, current_process.id))
            current_process.burst_time -= 1

    total_wait = 0
    for task in _process_list:
        #wait =  task.first_call - task.arrive_time 
        print(task.amount_waited())
        total_wait += task.amount_waited()
        #print(task.finish_time)
    avg_wait = total_wait / len(process_list)
    print(out_put)
    print(str(avg_wait))
    return (out_put,avg_wait)


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
    #RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    #write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    #SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    #write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])

