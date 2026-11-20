import { createFileRoute } from '@tanstack/react-router'
import { MediaPage } from '@/components/media/mediapage'

export const Route = createFileRoute('/media/$mediaId')({
  component: MediaDetailRoute,
})

function MediaDetailRoute() {
  const { mediaId } = Route.useParams()
  return <MediaPage mediaId={Number(mediaId)} />
}