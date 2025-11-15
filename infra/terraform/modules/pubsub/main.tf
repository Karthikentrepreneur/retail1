resource "google_pubsub_topic" "gst" {
  name = "gst-requests"
}

resource "google_pubsub_topic" "payments" {
  name = "payment-webhooks"
}

resource "google_pubsub_topic" "sync" {
  name = "sync-events"
}

resource "google_pubsub_subscription" "gst" {
  name                 = "gst-worker-sub"
  topic                = google_pubsub_topic.gst.name
  ack_deadline_seconds = 60
}

output "topics" {
  value = {
    gst      = google_pubsub_topic.gst.name
    payments = google_pubsub_topic.payments.name
    sync     = google_pubsub_topic.sync.name
  }
}
