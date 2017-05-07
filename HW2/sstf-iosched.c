/*
 * elevator sstf
 */

// THIS IS SSTF ELEVATOR IO SCHEDULER __NOT__ NOOP SCHEDULER 
// Authors: Brandon Dring, William Buffum, Samuel Jacobs


#include <linux/blkdev.h>
#include <linux/elevator.h>
#include <linux/bio.h>
#include <linux/module.h>
#include <linux/slab.h>
#include <linux/init.h>

/* Edited to track head position
 */
struct sstf_data {
        struct list_head queue;
	/* Needs to keep track of current head position
	 * To know not to backwards for new requests
	 */
	sector_t head_pos;        
};

static void sstf_merged_requests(struct request_queue *q, struct request *rq,
                                 struct request *next)
{
        list_del_init(&next->queuelist);
}

/* Edited to update head position on dispatch */
static int sstf_dispatch(struct request_queue *q, int force)
{
        struct sstf_data *nd = q->elevator->elevator_data;
 
        if (!list_empty(&nd->queue)) {
                struct request *rq;
                rq = list_entry(nd->queue.next, struct request, queuelist);
            	printk(KERN_ALERT "Dispatching request w/ sector no.: %lu\n",
                        rq_end_sector(rq));
                list_del_init(&rq->queuelist);
		/* update head position */
		nd->head_pos = rq_end_sector(rq);
                elv_Gdispatch_sort(q, rq);
                return 1;
        }
        return 0;
}

static void __print_request_queue(request_queue *q)
{
	struct sstf_data *nd = q->elevator->elevator_data;
        struct list_head *iter = NULL;
        struct request *tmp = NULL;
        /*Iterate thru each element already in request queue*/
	printk(KERN_ALERT "Printing Request Queue\nHead pos is %lu\n",
		nd->head_pos);
        list_for_each(iter, &nd->queue){
        	tmp = list_entry(iter, struct request, queuelist);
        	printk(KERN_ALERT "\tRequest w/ Section %lu \n"
				, blk_rq_pos(tmp));
	}
}

/* -----------------NEED TO CHANGE THIS------------------------------- */
static void sstf_add_request(struct request_queue *q, struct request *rq)
{
        struct sstf_data *nd = q->elevator->elevator_data;
        //sector_t cur; 
        printk(KERN_ALERT "Adding request w/ sector no.: %lu\n",
                        blk_rq_pos(rq));
        struct list_head *iter = NULL;
        struct request *tmp = NULL;
        /*Iterate thru each element already in request queue*/
        list_for_each(iter, &nd->queue){
        	tmp = list_entry(iter, struct request, queuelist);
//        	printk("Here is a req % lu \n", rq_end_sector(tmp));
		/* Insertion Sort 1 */
		if((blk_rq_pos(rq) > nd->head_pos)
		&& ((blk_rq_pos(rq) < blk_rq_pos(tmp))
		|| (blk_rq_pos(tmp) < nd->head_pos))){
			/* Found position for request
			 * Will be inserted on the head's current journey up
			 * and before a bigger request
			 * or if the end of the upward journey is reached
			 *, simply between the head position
			 * and the first request on the head's next journey up
			 */
			break;
		}
		/* Insertion Sort 2 */
		if((blk_rq_pos(tmp) < nd->head_pos)
		&& (blk_rq_pos(tmp) > blk_rq_pos(rq))){
			/* Assume list is already correctly sorted
			 * therefore "backend" of list is requests prepped
			 * for next upward journey
			 * Will therefore place new request in sorted order on
			 * backend
			 */
			break;
		}
	}
	/* At this point iteration was either broken because position for 
	 * insertion was found or exhausted (including empty or singular
	 * list case) 
	 * That means its time to insert the new request!
	 */
	list_add_tail(&rq->queuelist, iter);
	/* Note, even iteration quit before it began
	 * iter stil got assigned at least the sentinel of queue
	 */
	__print_request_queue(q);
}
/* -----------------Change me ----------------------------------- */




static struct request *
sstf_former_request(struct request_queue *q, struct request *rq)
{
        struct sstf_data *nd = q->elevator->elevator_data;

        if (rq->queuelist.prev == &nd->queue)
                return NULL;
        return list_entry(rq->queuelist.prev, struct request, queuelist);
}

static struct request *
sstf_latter_request(struct request_queue *q, struct request *rq)
{
        struct sstf_data *nd = q->elevator->elevator_data;

        if (rq->queuelist.next == &nd->queue)
                return NULL;
        return list_entry(rq->queuelist.next, struct request, queuelist);
}
/* Edited to initialize head position variable
 */
static int sstf_init_queue(struct request_queue *q, struct elevator_type *e)
{
        struct sstf_data *nd;
        struct elevator_queue *eq;

        eq = elevator_alloc(q, e);
        if (!eq)
                return -ENOMEM;

        nd = kmalloc_node(sizeof(*nd), GFP_KERNEL, q->node);
        if (!nd) {
                kobject_put(&eq->kobj);
                return -ENOMEM;
        }
	/* Added head position variable
	 * starts @ 0
	 */
	nd->head_pos = 0;
        eq->elevator_data = nd;

        INIT_LIST_HEAD(&nd->queue);

        spin_lock_irq(q->queue_lock);
        q->elevator = eq;
        spin_unlock_irq(q->queue_lock);
        return 0;
}

static void sstf_exit_queue(struct elevator_queue *e)
{
        struct sstf_data *nd = e->elevator_data;

        BUG_ON(!list_empty(&nd->queue));
        kfree(nd);
}

static struct elevator_type elevator_sstf = {
        .ops = {
                .elevator_merge_req_fn          = sstf_merged_requests,
                .elevator_dispatch_fn           = sstf_dispatch,
                .elevator_add_req_fn            = sstf_add_request,
                .elevator_former_req_fn         = sstf_former_request,
                .elevator_latter_req_fn         = sstf_latter_request,
                .elevator_init_fn               = sstf_init_queue,
                .elevator_exit_fn               = sstf_exit_queue,
        },
        .elevator_name = "sstf",
        .elevator_owner = THIS_MODULE,
};

static int __init sstf_init(void)
{
        return elv_register(&elevator_sstf);
}

static void __exit sstf_exit(void)
{
        elv_unregister(&elevator_sstf);
}

module_init(sstf_init);
module_exit(sstf_exit);


MODULE_AUTHOR("Jens Axboe");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("No-op IO scheduler");
