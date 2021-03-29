resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_cloudwatch_log_group" "example" {
  name              = "/aws/lambda/spotify_archiver"
  retention_in_days = 14
}

resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "src"
  output_path = "spotify_archiver.zip"
}

resource "aws_lambda_function" "spotify_archiver" {
  filename      = "spotify_archiver.zip"
  function_name = "spotify_archiver"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "app.lambda_handler"

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  runtime = "python3.8"

  environment {
    variables = {
      SPOTIFY_APP_ID        = var.spotify_app_id
      SPOTIFY_APP_SECRET    = var.spotify_app_secret
      PLAYLIST_1_ID         = var.playlist_1_id
      ARCHIVE_PLAYLIST_1_ID = var.archive_playlist_1_id
      PLAYLIST_2_ID         = var.playlist_2_id
      ARCHIVE_PLAYLIST_2_ID = var.archive_playlist_2_id
      PLAYLIST_3_ID         = var.playlist_3_id
      ARCHIVE_PLAYLIST_3_ID = var.archive_playlist_3_id
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs,
    aws_cloudwatch_log_group.example,
  ]
}

resource "aws_cloudwatch_event_rule" "every_thirty_minutes" {
  name                = "every-thirty-minutes"
  description         = "Fires every thirty minutes"
  schedule_expression = "rate(30 minutes)"
}

resource "aws_cloudwatch_event_target" "spotify_archiver_every_thirty_minutes" {
  rule      = aws_cloudwatch_event_rule.every_thirty_minutes.name
  target_id = "spotify_archiver"
  arn       = aws_lambda_function.spotify_archiver.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_spotify_archiver" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.spotify_archiver.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_thirty_minutes.arn
}